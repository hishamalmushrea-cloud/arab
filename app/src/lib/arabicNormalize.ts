// تطبيع عربي للبحث — يحافظ على المعنى، يزيل التشكيل للبحث
export function normalizeArabic(text: string): string {
  if (!text) return '';
  return text
    .toLowerCase()
    .replace(/[\u064B-\u065F]/g, '') // إزالة تشكيل
    .replace(/[إأآا]/g, 'ا')
    .replace(/ى/g, 'ي')
    .replace(/ة/g, 'ه')
    .replace(/ؤ/g, 'و')
    .replace(/ئ/g, 'ي')
    .replace(/\s+/g, ' ')
    .trim();
}

export function tokenizeArabic(text: string): string[] {
  const norm = normalizeArabic(text);
  return norm.split(' ').filter(Boolean);
}
