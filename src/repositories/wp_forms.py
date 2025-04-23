from sqlalchemy import select, func, cast, String, text, and_, or_
from sqlalchemy.orm import selectinload, with_loader_criteria
from src.configurations.constants import ALLOWED_QUESTION_TYPES, ALL_SEARCH_TAGS
from src.models.wp_forms import WPForm
from src.models.wp_fields import WPField


class WPFormRepository:
    def __init__(self, session):
        self.session = session

    async def get_all_forms(self) -> list[WPForm]:
        query = select(WPForm)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_form(self, form_id: int) -> WPForm | None:
        return await self.session.get(WPForm, form_id)

    async def get_all_forms_with_hash(self) -> list[tuple[WPForm, str]]:
        """
        Возвращает список кортежей (WPForm, questionnaire_hash), где questionnaire_hash вычисляется как
        SHA2( CONCAT( <данные из WPForm>, GROUP_CONCAT( SHA2( CONCAT( <данные из WPField> ), 512) ) ), 512)
        При этом сначала для сессии устанавливается большой лимит group_concat_max_len,
        а все NULL приводятся к '' через COALESCE.
        Также, форма загружается со всеми связанными WPField через relationship.
        """

        # Увеличиваем лимит только для этой сессии
        await self.session.execute(
            text("SET SESSION group_concat_max_len = :max_len")
            .bindparams(max_len=1_000_000_000)
        )

        # Поля из WPForm
        form_id = func.coalesce(cast(WPForm.id, String), '')
        form_key = func.coalesce(WPForm.form_key, '')
        form_name = func.coalesce(WPForm.name, '')
        form_descr = func.coalesce(WPForm.description, '')
        form_parent = func.coalesce(cast(WPForm.parent_form_id, String), '')
        form_logged = func.coalesce(cast(WPForm.logged_in, String), '')
        form_editable = func.coalesce(cast(WPForm.editable, String), '')
        form_is_template = func.coalesce(cast(WPForm.is_template, String), '')
        form_default_tpl = func.coalesce(cast(WPForm.default_template, String), '')
        form_status = func.coalesce(WPForm.status, '')
        form_options = func.coalesce(WPForm.options, '')
        form_created = func.coalesce(cast(WPForm.created_at, String), '')

        # Хеш каждой записи поля
        field_hash = func.sha2(
            func.concat(
                func.coalesce(cast(WPField.id, String), ''),
                func.coalesce(WPField.field_key, ''),
                func.coalesce(WPField.name, ''),
                func.coalesce(WPField.description, ''),
                func.coalesce(WPField.type, ''),
                func.coalesce(WPField.default_value, ''),
                func.coalesce(WPField.options, ''),
                func.coalesce(cast(WPField.field_order, String), ''),
                func.coalesce(cast(WPField.required, String), ''),
                func.coalesce(WPField.field_options, ''),
                func.coalesce(cast(WPField.form_id, String), ''),
                func.coalesce(cast(WPField.created_at, String), '')
            ),
            512
        )

        # Группируем хеши разрешённых полей
        field_concat_hashes = func.group_concat(
            field_hash
            .op("SEPARATOR")("")
        )

        # Общий questionnaire_hash
        questionnaire_hash = func.sha2(
            func.concat(
                form_id, form_key, form_name, form_descr, form_parent, form_logged, form_editable,
                form_is_template, form_default_tpl, form_status, form_options, form_created,
                func.coalesce(field_concat_hashes, '')
            ),
            512
        ).label("questionnaire_hash")

        # Условие соединения: только разрешённые типы полей
        join_cond = and_(
            WPField.form_id == WPForm.id,
            WPField.type.in_(ALLOWED_QUESTION_TYPES)
        )

        # Оставляем только те анкеты, у которых есть хотя бы один тег
        tag_filters = [
            WPForm.form_key.ilike(f"%{tag}%")
            for tag in ALL_SEARCH_TAGS
        ]

        query = (
            select(WPForm, questionnaire_hash)
            .where(or_(*tag_filters))
            .outerjoin(WPField, join_cond)
            .options(
                selectinload(WPForm.fields),
                with_loader_criteria(
                    WPField,
                    WPField.type.in_(ALLOWED_QUESTION_TYPES),
                    include_aliases=True
                ))
            .group_by(WPForm.id)
        )
        result = await self.session.execute(query)
        return result.all()
