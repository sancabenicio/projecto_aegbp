import React, { useState, useEffect } from 'react';
import Header from './Header';
import { Container, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';
import Footer from './Footer'; 
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const Faq = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/faqs/`;

    axios.get(apiUrl)
      .then(response => {
        setFaqs(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(t('faq.errorLoading')); // Usando tradução para mensagens de erro
        setLoading(false);
      });
  }, [t]);

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('faq.loading')}</span> {/* Usando tradução para o texto de carregamento */}
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!faqs || faqs.length === 0) {
    return <p className="text-center">{t('faq.noFaqsFound')}</p>; 
  }

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center' }}>
          {t('faq.title')} {/* Usando tradução para "Perguntas Frequentes" */}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000', textAlign: 'center', marginBottom: '30px' }}>
          {t('faq.subtitle')} {/* Usando tradução para o subtítulo */}
        </p>
        <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
          {faqs.map(faq => (
            <li key={faq.id} style={{ marginBottom: '20px', padding: '15px', borderBottom: '1px solid #ddd' }}>
              <h5 style={{ fontWeight: 'bold', color: '#333' }}>
                {faq.question || t('faq.noQuestionAvailable')} {/* Usando tradução para "Pergunta não disponível" */}
              </h5>
              <p style={{ margin: '10px 0', color: '#555' }}>
                {faq.answer || t('faq.noAnswerAvailable')} {/* Usando tradução para "Resposta não disponível" */}
              </p>
            </li>
          ))}
        </ul>
      </Container>
      <Footer />
    </div>
  );
};

export default Faq;
