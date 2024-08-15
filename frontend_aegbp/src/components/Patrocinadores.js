import React, { useState, useEffect } from 'react';
import Header from './Header';
import { Container, Row, Col, Spinner, Alert, Image } from 'react-bootstrap';
import axios from 'axios';
import Footer from './Footer';
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const Patrocinadores = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [patrocinadores, setPatrocinadores] = useState([]);
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
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/sponsors/`;

    axios.get(apiUrl)
      .then(response => {
        setPatrocinadores(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error(t('sponsors.errorFetchingSponsors'), error); // Usando tradução para mensagens de erro
        setError(t('sponsors.errorLoadingSponsorsList')); // Usando tradução para mensagens de erro
        setLoading(false);
      });
  }, [t]);

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('sponsors.loading')}</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!patrocinadores || patrocinadores.length === 0) {
    return <p className="text-center">{t('sponsors.noSponsorsFound')}</p>;
  }

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center', marginBottom: '40px' }}>
          {t('sponsors.title')} {/* Usando tradução para "Patrocinadores/Parceiros" */}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#555', textAlign: 'center', marginBottom: '40px' }}>
          {t('sponsors.subtitle')} {/* Usando tradução para subtítulo */}
        </p>
        <Row>
          {patrocinadores.map(patrocinador => (
            <Col md={6} className="mb-4" key={patrocinador.id}>
              <Row>
                <Col md={6} className="d-flex align-items-center justify-content-center">
                  <Image src={patrocinador.logo} alt={patrocinador.name} fluid style={{ maxHeight: '200px' }} />
                </Col>
                <Col md={6} className="d-flex flex-column justify-content-center">
                  <h5 style={{ fontWeight: 'bold', color: '#333' }}>
                    {patrocinador.name || t('sponsors.nameUnavailable')} {/* Usando tradução para "Nome do patrocinador não disponível" */}
                  </h5>
                  <p style={{ margin: '0.5rem 0', color: '#555' }}>
                    {patrocinador.description || t('sponsors.descriptionUnavailable')} {/* Usando tradução para "Descrição não disponível" */}
                  </p>
                </Col>
              </Row>
            </Col>
          ))}
        </Row>
      </Container>
      <Footer /> {/* Add Footer component */}
    </div>
  );
}

export default Patrocinadores;
