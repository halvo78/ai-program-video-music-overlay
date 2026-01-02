'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { api, ApiError, NetworkError } from './api'

// Hook for API requests with loading and error states
export function useApi<T>(
  fetcher: () => Promise<T>,
  deps: any[] = []
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetcher()
      setData(result)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`API Error (${err.status}): ${err.message}`)
      } else if (err instanceof NetworkError) {
        setError(`Network Error: ${err.message}`)
      } else {
        setError(String(err))
      }
    } finally {
      setLoading(false)
    }
  }, deps)

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return { data, loading, error, refetch: fetchData }
}

// Hook for debounced values
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}

// Hook for local storage persistence
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue
    }
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  const setValue = useCallback(
    (value: T | ((val: T) => T)) => {
      try {
        const valueToStore = value instanceof Function ? value(storedValue) : value
        setStoredValue(valueToStore)
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(key, JSON.stringify(valueToStore))
        }
      } catch (error) {
        console.warn(`Error setting localStorage key "${key}":`, error)
      }
    },
    [key, storedValue]
  )

  return [storedValue, setValue] as const
}

// Hook for interval polling
export function usePolling<T>(
  fetcher: () => Promise<T>,
  interval: number,
  enabled: boolean = true
) {
  const { data, loading, error, refetch } = useApi(fetcher, [])
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    if (enabled && interval > 0) {
      intervalRef.current = setInterval(refetch, interval)
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [enabled, interval, refetch])

  return { data, loading, error, refetch }
}

// Hook for workflow status tracking
export function useWorkflowStatus(workflowId: string | null) {
  const [status, setStatus] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  const fetchStatus = useCallback(async () => {
    if (!workflowId) return

    setLoading(true)
    try {
      const result = await api.getWorkflow(workflowId)
      setStatus(result)

      // Stop polling if workflow is complete
      if (result.status === 'completed' || result.status === 'failed') {
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
          intervalRef.current = null
        }
      }
    } catch (err) {
      setError(String(err))
    } finally {
      setLoading(false)
    }
  }, [workflowId])

  useEffect(() => {
    if (workflowId) {
      fetchStatus()
      intervalRef.current = setInterval(fetchStatus, 2000) // Poll every 2 seconds
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [workflowId, fetchStatus])

  return { status, loading, error }
}

// Hook for toast notifications
export function useToast() {
  const [toasts, setToasts] = useState<Array<{
    id: string
    type: 'success' | 'error' | 'info' | 'warning'
    message: string
  }>>([])

  const addToast = useCallback((
    type: 'success' | 'error' | 'info' | 'warning',
    message: string
  ) => {
    const id = Math.random().toString(36).substr(2, 9)
    setToasts(prev => [...prev, { id, type, message }])

    // Auto remove after 5 seconds
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id))
    }, 5000)
  }, [])

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  return { toasts, addToast, removeToast }
}

// Hook for form validation
export function useFormValidation<T extends Record<string, any>>(
  initialValues: T,
  validators: Partial<Record<keyof T, (value: any) => string | null>>
) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({})
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({})

  const setValue = useCallback((field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }))

    // Validate on change if already touched
    if (touched[field] && validators[field]) {
      const error = validators[field]!(value)
      setErrors(prev => ({
        ...prev,
        [field]: error || undefined
      }))
    }
  }, [touched, validators])

  const setFieldTouched = useCallback((field: keyof T) => {
    setTouched(prev => ({ ...prev, [field]: true }))

    // Validate on blur
    if (validators[field]) {
      const error = validators[field]!(values[field])
      setErrors(prev => ({
        ...prev,
        [field]: error || undefined
      }))
    }
  }, [values, validators])

  const validateAll = useCallback(() => {
    const newErrors: Partial<Record<keyof T, string>> = {}
    let isValid = true

    for (const [field, validator] of Object.entries(validators)) {
      if (validator) {
        const error = validator(values[field as keyof T])
        if (error) {
          newErrors[field as keyof T] = error
          isValid = false
        }
      }
    }

    setErrors(newErrors)
    return isValid
  }, [values, validators])

  const reset = useCallback(() => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
  }, [initialValues])

  return {
    values,
    errors,
    touched,
    setValue,
    setFieldTouched,
    validateAll,
    reset
  }
}
