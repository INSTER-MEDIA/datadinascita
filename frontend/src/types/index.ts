/**
 * Type definitions for DataDiNascita application.
 */

export interface User {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  timezone: string
  date_joined: string
}

export interface Contact {
  id: number
  name: string
  email: string
  phone: string
  birthday: string | null
  photo: string | null
  notes: string
  age: number | null
  next_birthday: string | null
  days_until_birthday: number | null
  upcoming_age: number | null
  created_at: string
  updated_at: string
}

export interface ContactList {
  id: number
  name: string
  birthday: string | null
  days_until_birthday: number | null
  upcoming_age: number | null
}

export interface Event {
  id: number
  type: 'birthday' | 'anniversary' | 'holiday' | 'other'
  name: string
  date: string
  recurs_annually: boolean
  notify_days_before: number
  notes: string
  next_occurrence: string
  days_until_next: number
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  password_confirm: string
  first_name?: string
  last_name?: string
  timezone?: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
