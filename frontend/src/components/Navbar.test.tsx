// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest'
import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Navbar } from './Navbar'

describe('Navbar Component (#241)', () => {
  const defaultProps = {
    theme: 'dark' as const,
    toggleTheme: vi.fn(),
    user: null,
    onLogin: vi.fn(),
    onLogout: vi.fn(),
    onHistoryClick: vi.fn(),
  }

  it('renders the header brand with emoji and "AI Resume Analyzer" title text', () => {
    render(<Navbar {...defaultProps} />)
    const brandElement = screen.getByText('AI Resume Analyzer')
    expect(brandElement).toBeInTheDocument()
    expect(screen.getByText('🚀')).toBeInTheDocument()
  })

  it('renders correctly in light mode', () => {
    render(<Navbar {...defaultProps} theme="light" />)
    expect(screen.getByText('AI Resume Analyzer')).toBeInTheDocument()
  })
})

describe('Navbar Component right-side cluster (#244)', () => {
  it('renders all right-side cluster elements without clipping issues', () => {
    render(
      <Navbar
        theme="light"
        toggleTheme={() => {}}
        user={null}
        onLogin={() => {}}
        onLogout={() => {}}
        onHistoryClick={() => {}}
      />
    )

    const loginBtn = screen.getByRole('button', { name: /login \/ sign up/i })
    expect(loginBtn).toBeInTheDocument()
    expect(loginBtn).toHaveClass('auth-bar-btn')

    const themeBtn = screen.getByRole('button', { name: /toggle theme/i })
    expect(themeBtn).toBeInTheDocument()
    expect(themeBtn).toHaveClass('theme-toggle-navbar')
  })

  it('renders user profile when user is authenticated', () => {
    const user = { username: 'testuser', token: 'fake-token' }
    render(
      <Navbar
        theme="dark"
        toggleTheme={() => {}}
        user={user}
        onLogin={() => {}}
        onLogout={() => {}}
        onHistoryClick={() => {}}
      />
    )

    expect(screen.getByText(/testuser/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument()
  })
})
