/** True only when a real Clerk publishable key is configured. Placeholders do not count. */
export function isClerkConfigured(): boolean {
  const key = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? '';
  return key.startsWith('pk_') && !key.includes('YOUR');
}
