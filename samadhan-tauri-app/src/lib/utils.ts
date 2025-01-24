export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US', {
    notation: value > 9999 ? 'compact' : 'standard',
    maximumFractionDigits: 1,
  }).format(value);
}

export function formatTime(minutes: number): string {
  // Round minutes to nearest integer
  minutes = Math.round(minutes);
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours === 0) {
    return `${mins}m`;
  }
  return mins === 0 ? `${hours}h` : `${hours}h ${mins}m`;
}

export function cn(...classes: (string | undefined)[]) {
  return classes.filter(Boolean).join(' ');
} 