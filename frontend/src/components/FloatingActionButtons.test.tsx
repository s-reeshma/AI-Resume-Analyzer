// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import React from 'react'
import { HistorySidebar } from '../HistorySidebar'
import type { AnalysisEntry } from '../hooks/useAnalysisHistory'

const mockEntries: AnalysisEntry[] = [
  {
    id: '1',
    timestamp: 1000,
    score: 85,
    skills: ['React', 'TypeScript'],
    suggestions: ['Improve summary'],
    matchedSkills: ['React'],
    missingSkills: ['Vue'],
    targetRole: 'Frontend Developer',
    fileName: 'resume1.pdf',
  },
]

describe('Unified Floating Action Buttons (#247)', () => {
  it('renders HistorySidebar FAB with shared fab-btn class and accessible attributes', () => {
    const handleToggle = vi.fn()
    render(
      <HistorySidebar
        entries={mockEntries}
        isOpen={false}
        onToggle={handleToggle}
        onSelect={() => {}}
        onDelete={() => {}}
        onClear={() => {}}
      />
    )

    const historyFab = screen.getByRole('button', {
      name: /open history/i,
    })

    expect(historyFab).toBeInTheDocument()
    expect(historyFab).toHaveClass('fab-btn')
    expect(historyFab).toHaveClass('history-toggle-btn')
    expect(historyFab).toHaveAttribute('aria-expanded', 'false')
    expect(historyFab).toHaveAttribute('title', 'View history')

    fireEvent.click(historyFab)
    expect(handleToggle).toHaveBeenCalledTimes(1)
  })

  it('renders open HistorySidebar FAB with aria-expanded="true"', () => {
    render(
      <HistorySidebar
        entries={mockEntries}
        isOpen={true}
        onToggle={() => {}}
        onSelect={() => {}}
        onDelete={() => {}}
        onClear={() => {}}
      />
    )

    const historyFab = screen.getByRole('button', {
      name: /close history/i,
    })

    expect(historyFab).toBeInTheDocument()
    expect(historyFab).toHaveClass('fab-btn')
    expect(historyFab).toHaveAttribute('aria-expanded', 'true')
    expect(historyFab).toHaveAttribute('title', 'Close history')
  })
})
