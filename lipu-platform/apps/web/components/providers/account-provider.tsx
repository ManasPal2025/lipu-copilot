'use client';

import { useAuth, useUser } from '@clerk/nextjs';
import { createContext, useContext, useMemo, useRef } from 'react';

export type AccountUser = {
  firstName: string | null;
  lastName: string | null;
  email: string | null;
  phone: string | null;
  imageUrl: string | null;
};

export type AccountValue = {
  status: 'loading' | 'guest' | 'authenticated';
  user: AccountUser | null;
  getToken: () => Promise<string | null>;
  signOut: () => Promise<void>;
};

const guestAccount: AccountValue = {
  status: 'guest',
  user: null,
  getToken: async () => null,
  signOut: async () => undefined,
};

const AccountContext = createContext<AccountValue>(guestAccount);

export function useAccount(): AccountValue {
  return useContext(AccountContext);
}

export function AccountStateProvider({
  value,
  children,
}: {
  value: AccountValue;
  children: React.ReactNode;
}) {
  return <AccountContext.Provider value={value}>{children}</AccountContext.Provider>;
}

export function ClerkAccountProvider({ children }: { children: React.ReactNode }) {
  const { isLoaded, isSignedIn, user } = useUser();
  const { getToken, signOut } = useAuth();
  const getTokenRef = useRef(getToken);
  const signOutRef = useRef(signOut);
  getTokenRef.current = getToken;
  signOutRef.current = signOut;
  const firstName = user?.firstName ?? null;
  const lastName = user?.lastName ?? null;
  const email = user?.primaryEmailAddress?.emailAddress ?? null;
  const phone = user?.primaryPhoneNumber?.phoneNumber ?? null;
  const imageUrl = user?.imageUrl ?? null;

  const value = useMemo<AccountValue>(() => {
    if (!isLoaded) {
      return {
        status: 'loading',
        user: null,
        getToken: async () => null,
        signOut: async () => undefined,
      };
    }
    if (!isSignedIn) {
      return guestAccount;
    }
    return {
      status: 'authenticated',
      user: {
        firstName,
        lastName,
        email,
        phone,
        imageUrl,
      },
      getToken: async () => (await getTokenRef.current()) ?? null,
      signOut: async () => {
        await signOutRef.current({ redirectUrl: '/' });
      },
    };
  }, [email, firstName, imageUrl, isLoaded, isSignedIn, lastName, phone]);

  return <AccountContext.Provider value={value}>{children}</AccountContext.Provider>;
}
