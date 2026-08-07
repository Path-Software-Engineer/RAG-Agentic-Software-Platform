export function formatScore(score: number): string {
  return score.toFixed(3);
}

export function formatLocator(locator: Record<string, unknown>): string {
  if (locator.kind === 'character_range') {
    return `Characters ${locator.start ?? '?'}-${locator.end ?? '?'}`;
  }
  return 'Source location available';
}
