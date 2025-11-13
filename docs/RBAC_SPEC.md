# RBAC & Organization Model Specification

Этот документ описывает целевую модель многоарендности и управления правами для Task Tracker. Реализация входит в Phase 2 дорожной карты Jira-паритета.

## 1. Цели
1. **Tenant Isolation** — каждый пользователь видит только организации/проекты, где он состоит.
2. **Ролевое управление** — гибкое назначение прав на уровне организации и проекта.
3. **Масштабируемость** — возможность добавления кастомных ролей/прав в будущем.
4. **Аудит** — фиксировать, кто и когда выдаёт права.

## 2. Сущности

### Users
Без изменений в схеме, но добавляем поля профиля (позже).

### Organizations
- `id`, `name`, `slug`, `owner_id`.
- Новое поле `default_role` (по умолчанию `member`).

### Organization Membership (`user_organizations`)
| Поле | Тип | Комментарий |
| --- | --- | --- |
| `user_id` | UUID | PK (совместно). |
| `organization_id` | UUID | PK (совместно). |
| `role` | Enum (`owner`, `admin`, `member`, `viewer`) | Роль в организации. |
| `permissions` | JSONB (nullable) | Переопределения по пользователю. |
| `joined_at` | timestamp | Уже есть. |

### Projects
- `organization_id` (уже есть).
- Новые поля: `lead_id` (UUID), `workflow_id` (UUID), `key_sequence` (INT, для concurrency safe task numbers).

### Project Membership (`project_members`)
| Поле | Тип | Комментарий |
| --- | --- | --- |
| `project_id` | UUID | PK часть. |
| `user_id` | UUID | PK часть. |
| `role` | Enum (`lead`, `developer`, `viewer`, `guest`) | Можно расширять. |
| `permissions` | JSONB | Переопределения (например, доступ к настройкам). |
| `added_by` | UUID | Кто пригласил. |
| `added_at` | timestamp | Уже есть. |

### Workflow / Permissions
- Таблица `workflows` (id, organization_id, name, type, default_flag).
- Таблица `workflow_statuses` (id, workflow_id, key, name, order, category).
- Таблица `workflow_transitions` (id, workflow_id, from_status_id, to_status_id, allowed_roles).
- Таблица `permission_schemes` + `permission_scheme_rules` (гранулярные права типа «browse projects», «edit issues»).
- Projects ссылаются на `workflow_id` и `permission_scheme_id`.

## 3. Роли и права

### Organization Roles
- `owner`: полный доступ, управление биллингом.
- `admin`: управление пользователями/проектами внутри организации.
- `member`: стандартный доступ (участие в проектах, создание задач, но не управление организацией).
- `viewer`: только чтение проектов/задач.

### Project Roles
- `lead`: управление проектом + настройками.
- `developer`: создание/редактирование тасков, переходы по workflow.
- `viewer`: только чтение.
- `guest`: ограниченный просмотр (например, только выбранные эпики).

### Permission Groups (для схем)
1. **Browse Projects**
2. **View Issues**
3. **Create Issues**
4. **Edit Issues**
5. **Transition Issues**
6. **Schedule Issues (sprints)**
7. **Manage Sprints**
8. **Administer Project**
9. **Comment / Delete Comment**
10. **Service permissions** — интеграции, вебхуки, automation.

Каждая роль мапится на набор permission groups; схемы позволяют менять соответствия без переписывания кода.

## 4. API Изменения

### Middleware / Dependencies
- `get_current_user` остаётся, но добавляются:
  - `get_current_org_member(org_id)`: проверяет, что пользователь состоит в организации.
  - `get_current_project_member(project_id, required_permission)`.
- Декораторы/утилиты для проверки прав (например, `@requires_permission("EDIT_ISSUES")`).

### Auth Flow
- После логина клиент запрашивает `/me/organizations` и `/me/projects` для построения навигации.
- Добавить endpoint для переключения текущей организации (для последующего UX).

### Invitation Flow
- POST `/organizations/{id}/members` для приглашений.
- POST `/projects/{id}/members`.
- Подтверждение приглашений (ссылка/email или прямое добавление админом).

## 5. Миграции (итеративно)
1. **Step 1**: Добавить перечисленные поля и таблицы (`workflows`, `permission_schemes`) без использования.
2. **Step 2**: Заполнить дефолтные записи (Workflow «Software Simplified», Permission Scheme «Default»).
3. **Step 3**: Обновить CRUD так, чтобы проекты автоматически создавали `project_members` и `project_roles`.
4. **Step 4**: Включить проверки во всех эндпоинтах (tasks, projects, comments).
5. **Step 5**: Удалить временные заглушки (жёсткий `organization_id`) из фронтенда.

## 6. Backlog для реализации
- [ ] Миграция `2024xxxx_add_rbac_core.py`.
- [ ] CRUD для организаций/приглашений.
- [ ] Permission middleware.
- [ ] API `/workflows`, `/permission-schemes`.
- [ ] UI: переключение организаций, управление участниками, настройка прав.

Документ следует обновлять по мере принятия архитектурных решений и реализации. Все PR, связанные с безопасностью и правами, должны ссылаться на соответствующий раздел данной спецификации.
