import type { Metadata } from 'next';
import './globals.css';
import ResearchToggle from '@/components/ResearchToggle';

export const metadata: Metadata = {
  title: 'موسوعة العرب - مشروع العرب Schema 2.0.0',
  description: 'موسوعة جغرافية وثقافية موثقة للدول العربية الـ22 - 5317 كيان، 151 مصدر، 2245 معلومة موثقة',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body className="min-h-screen">
        <header className="sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <a href="/" className="flex items-center gap-3">
              <div className="w-9 h-9 bg-gradient-to-br from-green-600 to-emerald-800 rounded-lg flex items-center justify-center text-white font-bold">ع</div>
              <div>
                <div className="font-bold text-lg leading-none">موسوعة العرب</div>
                <div className="text-xs text-gray-500">Schema 2.0.0 - 22 دولة - Offline</div>
              </div>
            </a>
            <nav className="flex items-center gap-4 text-sm">
              <a href="/" className="hover:text-green-700">الرئيسية</a>
              <a href="/countries" className="hover:text-green-700">الدول</a>
              <a href="/search" className="hover:text-green-700">البحث</a>
              <a href="/coverage" className="hover:text-green-700">التغطية</a>
              <a href="/sources" className="hover:text-green-700">المصادر</a>
              <ResearchToggle />
            </nav>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 py-6">
          {children}
        </main>
        <footer className="border-t border-gray-200 mt-12 py-8">
          <div className="max-w-7xl mx-auto px-4 text-sm text-gray-500 flex flex-wrap gap-4 justify-between">
            <div>
              <div>موسوعة العرب — بيانات موثقة Schema 2.0.0</div>
              <div>5317 كيان، 3261 اسم بديل، 5706 علاقة، 2245 ادعاء، 151 مصدر — 100% محفوظة</div>
            </div>
            <div className="ltr text-xs font-mono">
              <div>Release: generated/metadata.json</div>
              <div>App Bundle: app/public/data/app-data.json</div>
              <div>Test: test_app_data_completeness.py PASS</div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
