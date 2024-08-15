import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const Depoimentos = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [depoimentos, setDepoimentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/testimonials/`;

    axios.get(apiUrl)
      .then(response => {
        setDepoimentos(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(t('testimonials.errorLoading')); // Usando tradução para mensagens de erro
        setLoading(false);
      });
  }, [t]);

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('testimonials.loading')}</span> {/* Usando tradução para o texto de carregamento */}
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!depoimentos || depoimentos.length === 0) {
    return <p className="text-center">{t('testimonials.noTestimonialsFound')}</p>; 
  }

  return (
    <div>
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center' }}>
          {t('testimonials.title')} {/* Usando tradução para "Depoimentos" */}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000', textAlign: 'center', marginBottom: '40px' }}>
          {t('testimonials.subtitle')} {/* Usando tradução para o subtítulo */}
        </p>
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {depoimentos.map(depoimento => (
            <li key={depoimento.id} style={{ marginBottom: '30px', padding: '20px', borderBottom: '1px solid #ddd' }}>
              <Row>
                <Col md={3} sm={12}>
                  <h5 style={{ fontWeight: 'bold', color: '#333' }}>
                    {depoimento.name || t('testimonials.noNameAvailable')} {/* Usando tradução para "Nome não disponível" */}
                  </h5>
                  <p style={{ fontSize: '0.9rem', color: '#999' }}>
                    {depoimento.date || t('testimonials.noDateAvailable')} {/* Usando tradução para "Data não disponível" */}
                  </p>
                </Col>
                <Col md={9} sm={12}>
                  <p style={{ fontSize: '1rem', color: '#555' }}>
                    {depoimento.content || t('testimonials.noContentAvailable')} {/* Usando tradução para "Conteúdo não disponível" */}
                  </p>
                </Col>
              </Row>
            </li>
          ))}
        </ul>
      </Container>
    </div>
  );
};

export default Depoimentos;
