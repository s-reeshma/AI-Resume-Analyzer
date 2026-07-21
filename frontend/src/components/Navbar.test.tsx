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
