import React, { useState, useEffect } from 'react';
import Header from './Header';
import { Container, Spinner, Alert, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import Footer from './Footer';
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const Projetos = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [projetos, setProjetos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para extrair o prefixo de idioma da URL
  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//); // Captura o primeiro segmento do caminho
    return match ? match[1] : 'en'; // Retorna 'en' como padrão se não encontrar
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/projects/`;

    axios.get(apiUrl)
      .then(response => {
        setProjetos(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error(t('projects.errorFetchingProjects'), error); // Usando tradução para mensagens de erro
        setError(t('projects.errorLoadingProjects')); // Usando tradução para mensagens de erro
        setLoading(false);
      });
  }, [t]);

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('projects.loading')}</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!projetos || projetos.length === 0) {
    return <p className="text-center">{t('projects.noProjectsFound')}</p>;
  }

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center', marginBottom: '40px' }}>
          {t('projects.title')} {/* Usando tradução para "Projetos" */}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000', textAlign: 'center', marginBottom: '40px' }}>
          {t('projects.subtitle')} {/* Usando tradução para subtítulo */}
        </p>
        {projetos.map(projeto => (
          <Row key={projeto.id} className="mb-4 align-items-center">
            <Col md={12}>
              <h3 style={{ fontWeight: 'bold', color: '#333', borderBottom: '2px solid #FFD700', paddingBottom: '10px' }}>
                {projeto.title || t('projects.titleUnavailable')} {/* Usando tradução para "Título não disponível" */}
              </h3>
              <p style={{ marginTop: '10px', color: '#555', fontSize: '1.1rem' }}>
                <strong>{t('projects.startDate')}:</strong> {projeto.start_date || t('projects.startDateUnavailable')} {/* Usando tradução para "Data de início não disponível" */}
              </p>
              <p style={{ color: '#555', fontSize: '1.1rem' }}>
                <strong>{t('projects.endDate')}:</strong> {projeto.end_date || t('projects.endDateUnavailable')} {/* Usando tradução para "Data de término não disponível" */}
              </p>
              <p style={{ color: '#555', fontSize: '1.1rem' }}>
                <strong>{t('projects.description')}:</strong> {projeto.description || t('projects.descriptionUnavailable')} {/* Usando tradução para "Descrição não disponível" */}
              </p>
            </Col>
          </Row>
        ))}
      </Container>
      <Footer />
    </div>
  );
}

export default Projetos;
