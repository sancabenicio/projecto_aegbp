import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import translationEN from './locales/en/translation.json';
import translationPT from './locales/pt/translation.json';

const resources = {
  en: {
    translation: translationEN
  },
  pt: {
    translation: translationPT
  }
};

i18n
  .use(LanguageDetector) // Detecta automaticamente a linguagem do navegador
  .use(initReactI18next)  // Inicializa o i18next com o react-i18next
  .init({
    resources,
    fallbackLng: 'pt', // Define o fallback para Português
    lng: 'pt', // Idioma padrão inicial
    detection: {
      order: ['querystring', 'cookie', 'localStorage', 'navigator', 'htmlTag', 'path', 'subdomain'],
      caches: ['cookie', 'localStorage']
    },
    interpolation: {
      escapeValue: false // React já faz a sanitização
    }
  });

export default i18n;
