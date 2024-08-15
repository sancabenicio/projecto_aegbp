import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Home from './components/Home';
import Sobre from './components/Sobre';
import GaleriaFotos from './components/GaleriaFotos';
import GaleriaVideos from './components/GaleriaVideos';
import Calendario from './components/Calendario';
import Documentos from './components/Documentos';
import Blog from './components/Blog';
import Depoimentos from './components/Depoimentos';
import Faq from './components/Faq';
import Voluntariado from './components/Voluntariado';
import Projetos from './components/Projetos';
import Doacoes from './components/Doacoes';
import Patrocinadores from './components/Patrocinadores';
import Contatos from './components/Contatos';
import BlogPost from './components/BlogPost';
import RegisterMember from './components/RegisterMember';
import Page from './components/Page';
import './i18n';
import { useTranslation } from 'react-i18next'; // Importação do hook de tradução

const AppWithNavigate = () => {
  const navigate = useNavigate();
  const { i18n } = useTranslation(); // Hook de tradução para poder alterar o idioma

  useEffect(() => {
    const path = window.location.pathname;
    const match = path.match(/^\/[a-z]{2}\//); // Verifica se a URL já contém o prefixo de idioma

    if (!match) {
      // Detecta o idioma do navegador
      const browserLanguage = navigator.language.split('-')[0]; // Extrai o idioma, ex: 'pt' de 'pt-BR'
      const supportedLanguages = ['pt', 'en']; // Lista dos idiomas suportados
      const defaultLanguage = supportedLanguages.includes(browserLanguage) ? browserLanguage : 'pt'; // Usa o idioma do navegador ou 'pt' como fallback

      // Define o idioma no i18n e redireciona para a URL com o prefixo de idioma correto
      i18n.changeLanguage(defaultLanguage);
      navigate(`/${defaultLanguage}${path}`, { replace: true });
    } else {
      // Se o prefixo de idioma estiver presente na URL, sincroniza com o i18n
      const currentLanguageInURL = match[1];
      if (i18n.language !== currentLanguageInURL) {
        i18n.changeLanguage(currentLanguageInURL);
      }
    }
  }, [i18n, navigate]);

  return (
    <Routes>
      {/* Definindo uma rota base para o idioma */}
      <Route path="/:lang/" element={<Home />} />
      <Route path="/:lang/sobre" element={<Page><Sobre /></Page>} />
      <Route path="/:lang/galeria-fotos" element={<GaleriaFotos />} />
      <Route path="/:lang/galeria-videos" element={<GaleriaVideos />} />
      <Route path="/:lang/calendario" element={<Page><Calendario /></Page>} />
      <Route path="/:lang/documentos" element={<Documentos />} />
      <Route path="/:lang/blog" element={<Page><Blog /></Page>} />
      <Route path="/:lang/blog/:id" element={<BlogPost />} />
      <Route path="/:lang/depoimentos" element={<Page><Depoimentos /></Page>} />
      <Route path="/:lang/faq" element={<Faq />} />
      <Route path="/:lang/voluntariado" element={<Voluntariado />} />
      <Route path="/:lang/projetos" element={<Projetos />} />
      <Route path="/:lang/doacoes" element={<Doacoes />} />
      <Route path="/:lang/patrocinadores" element={<Patrocinadores />} />
      <Route path="/:lang/contatos" element={<Page><Contatos /></Page>} />
      <Route path="/:lang/membros" element={<RegisterMember />} />
    </Routes>
  );
};

const App = () => {
  return (
    <Router>
      <AppWithNavigate />
    </Router>
  );
};

export default App;
