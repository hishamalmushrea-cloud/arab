import { create } from 'zustand';

interface AppState {
  researchMode: boolean;
  toggleResearchMode: () => void;
  setResearchMode: (v: boolean) => void;
  dbReady: boolean;
  setDbReady: (v: boolean) => void;
  counts: Record<string, number> | null;
  setCounts: (c: Record<string, number>) => void;
}

export const useAppStore = create<AppState>((set) => ({
  researchMode: false,
  toggleResearchMode: () => set(s => {
    const next = !s.researchMode;
    if (typeof window !== 'undefined') localStorage.setItem('researchMode', String(next));
    return { researchMode: next };
  }),
  setResearchMode: (v) => set({ researchMode: v }),
  dbReady: false,
  setDbReady: (v) => set({ dbReady: v }),
  counts: null,
  setCounts: (c) => set({ counts: c }),
}));

// Load research mode from localStorage on client
if (typeof window !== 'undefined') {
  const saved = localStorage.getItem('researchMode');
  if (saved) {
    useAppStore.setState({ researchMode: saved === 'true' });
  }
}
