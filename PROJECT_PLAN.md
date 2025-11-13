# Jira Parity Implementation Plan

Дорожная карта, которая превращает TaskTracker в полноценный аналог Jira. План делится на фазы; внутри каждой перечислены ключевые блоки работы и критерии готовности.

## Phase 1 – Foundations
- **Требования и дизайн**: зафиксировать доменные сущности (организации, проекты, workflow, разрешения, sprints, backlog, notifications) и утвердить рабочие сценарии (scrum/kanban, software & design проекты).
- **Инфраструктура**: убрать auto-create таблиц из FastAPI, оставить только Alembic; добавить .env шаблон; подготовить make-команды для миграций/фикстур.
- **Тесты и качество**: включить pytest/vitest, smoke-тесты для health/auth, linters в CI, pre-commit. Настроить docker-compose override для локальной разработки.
- **Документация**: README + PROJECT_OVERVIEW отражают фактические возможности, есть раздел «что готово/в работе».

## Phase 2 – Backend Core
- **RBAC и принадлежность**: модели UserOrg, ProjectMember с ролями (owner, admin, developer, viewer); middleware, который ограничивает доступ.
- **Workflows**: статусы/переходы настраиваются на уровне проекта, поддерживаются несколько колонок, разрешения на переходы.
- **Backlog & Sprints**: API для backlog ordering, спринтов (plan/start/complete), burndown данных, story points.
- **Задачи и связи**: подзадачи, эпики, issue links (blocks/is blocked by/related), watchers, последний history trail.
- **Комментарии и вложения**: CRUD + rich metadata, упоминания, S3/MinIO storage, лимит размеров, thumbnail генерация.
- **Поиск**: полнотекстовый поиск по задачам и комментариям (PostgreSQL tsvector), базовый фильтр «как JQL-light».
- **События**: сервис уведомлений (Redis stream / Celery), audit log.

## Phase 3 – Frontend Core (Vue 3 + Tailwind)
- **Shell в стиле Atlassian**: левое меню (Projects, Filters, Dashboards), верхняя панель с глобальным поиском, переключатели организаций.
- **Backlog view**: drag&drop порядка, спринты, estimation, быстрые фильтры, контекстные действия.
- **Board view**: конфигурируемые колонки, swimlanes, аватары, WIP подсветка, инлайн переходы и assign.
- **Issue detail**: боковая панель + центральная область, полноценное редактирование (описание, поля, кастомные поля, вложения, ссылки, история).
- **Filters/Search**: сохранённые фильтры, панель условий (assignee, label, status, sprint). Глобальный поиск с подсказками.
- **Auth UX**: refresh-токены, восстановление пароля, профили.

## Phase 4 – Collaboration & Realtime
- **Notifications**: центр уведомлений во фронте, email/web push, настройки.
- **Realtime**: WebSocket на канбан доске, комментариях, watchers; optimistic updates с подтверждением.
- **Automation**: вебхуки, интеграция со Slack/Telegram, API-токены.
- **Monitoring**: Sentry, Prometheus metrics, структурированные логи.

## Phase 5 – Polish & Release
- **Analytics**: velocity, burndown, cumulative flow, workload, SLA отчёты.
- **Docs**: гайды для админов/проектов, API reference (генерация из FastAPI + примеры).
- **QA**: e2e тесты (Playwright/Cypress), нагрузочные тесты, security review.
- **Deployment**: Helm чарты / Terraform, миграции и seed-скрипты, backup/restore.

## Immediate Priorities (Sprint 1)
1. **Безопасность/Org Control**
   - Доделать RBAC из `docs/RBAC_SPEC.md`: роли owner/admin/member/guest, проверки на каждом endpoint.
   - Механизм приглашений + валидация принадлежности при создании проектов и задач (частично готово).
   - Реализовать refresh-token flow во фронте, хранение с автопродлением сессионных данных.
2. **Backlog & Board**
   - REST для backlog ordering, спринтов (create/start/complete), velocity калькуляции.
   - Обновить Kanban фронт: конфигурируемые статусы из workflow, swimlanes (assignee, epic).
   - Инлайн-редактор карточек (assignee, story points, due date, labels).
3. **Issue View & Collaboration**
   - Полноценная карточка задачи: tabs `Details`, `Activity`, `History`, `Attachments`.
   - Комментарии с упоминаниями, markdown, вложениями (S3/MinIO).
   - Watchers + уведомления (email/реактив через WebSocket).
4. **Quality & Tooling**
   - Расширить pytest (API-level, RBAC regression), запустить GitHub Actions.
   - Подключить vitest/Playwright smoke-тесты для auth/board.
   - Sentry + структурированные логи (опционально в конце спринта).

Каждая задача должна завершаться обновлением `PROJECT_OVERVIEW.md` и соответствующего чек-листа фазы. Спринт считается закрытым, когда security, backlog, issue view и базовые тесты покрывают новые сценарии.

## Ближайшие задачи (Sprint 0)
1. Удалить создание схем на старте приложения, оставить Alembic как единственный источник истины.
2. Обновить README/PROJECT_OVERVIEW, чтобы отражать текущую функциональность и ссылаться на этот план.
3. Настроить базовый каркас тестов (pytest + тест окружения).
4. Запланировать RBAC/Org модель и подготовить миграцию (спецификация схемы).

После выполнения списка Sprint 0 переходим к Phase 2 (backend core). Для контроля прогресса каждый pull request должен ссылаться на раздел/подзадачу из плана.
