export interface User {
  id: string
  email: string
  username: string
  first_name?: string
  last_name?: string
  avatar_url?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  last_login_at?: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
  first_name?: string
  last_name?: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export type TaskStatus = 'backlog' | 'todo' | 'in_progress' | 'review' | 'testing' | 'done' | 'cancelled'
export type TaskPriority = 'low' | 'medium' | 'high' | 'critical'
export type TaskType = 'task' | 'bug' | 'feature' | 'improvement' | 'epic' | 'story'

export interface Task {
  id: string
  project_id: string
  task_number: number
  title: string
  description?: string
  status: TaskStatus
  priority: TaskPriority
  type: TaskType
  assignee_id?: string
  reporter_id: string
  parent_task_id?: string
  sprint_id?: string
  due_date?: string
  estimated_hours?: number
  logged_hours: number
  story_points?: number
  tags?: string[]
  position: number
  created_at: string
  updated_at?: string
  resolved_at?: string
}

export interface Project {
  id: string
  organization_id: string
  name: string
  key: string
  description?: string
  status: string
  start_date?: string
  end_date?: string
  budget?: number
  created_by: string
  created_at: string
  updated_at?: string
}

export interface Comment {
  id: string
  task_id: string
  user_id: string
  parent_comment_id?: string
  content: string
  mentioned_users?: string[]
  edited: boolean
  created_at: string
  updated_at?: string
}

export interface Organization {
  id: string
  name: string
  slug: string
  description?: string
  logo_url?: string
  owner_id: string
  created_at: string
  updated_at?: string
}
