'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface ThemeToggleProps {
  className?: string;
  inverted?: boolean;
}

export function ThemeToggle({ className, inverted = false }: ThemeToggleProps) {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  if (!mounted) {
    return (
      <Button variant="ghost" size="icon" className={className} aria-label="Toggle theme" disabled>
        <Sun className="h-4 w-4" />
      </Button>
    );
  }

  const isDark = (theme === 'system' ? resolvedTheme : theme) === 'dark';

  return (
    <Button
      variant="ghost"
      size="icon"
      className={cn(inverted && 'text-stone-100 hover:bg-white/10 hover:text-white', className)}
      onClick={() => setTheme(isDark ? 'light' : 'dark')}
      aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  );
}
