'use client';
import { useEffect, useState } from 'react';

export default function ResearchToggle() {
  const [on, setOn] = useState(false);

  useEffect(() => {
    setOn(localStorage.getItem('researchMode') === 'true');
  }, []);

  return (
    <div className="flex items-center gap-2 border rounded-full px-3 py-1">
      <span className="text-xs">وضع الباحث</span>
      <button
        className={`w-8 h-4 rounded-full relative transition-colors ${on ? 'bg-green-600' : 'bg-gray-200'}`}
        onClick={() => {
          const next = !on;
          setOn(next);
          localStorage.setItem('researchMode', String(next));
          window.location.reload();
        }}
        aria-label="toggle research mode"
      >
        <span className={`absolute top-0.5 w-3 h-3 bg-white rounded-full shadow transition-all ${on ? 'left-4' : 'left-0.5'}`} />
      </button>
    </div>
  );
}
