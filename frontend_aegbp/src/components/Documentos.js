import React, { useState, useEffect } from 'react';
import Header from './Header';
import { Container, Row, Col, Spinner, Alert, Button } from 'react-bootstrap';
import axios from 'axios';
import Footer from './Footer'; 
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const Documentos = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [documentos, setDocumentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en'; 
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/documents/`;

    axios.get(apiUrl)
      .then(response => {
        setDocumentos(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(t('documents.errorLoading')); // Usando tradução para mensagens de erro
        setLoading(false);
      });
  }, [t]);

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('documents.loading')}</span> {/* Usando tradução para o texto de carregamento */}
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!documentos || documentos.length === 0) {
    return <p className="text-center">{t('documents.noDocumentsFound')}</p>; 
  }

  return (
    <div>
      <Header />
      <Container className="py-5">
        <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#006400', textAlign: 'center', marginBottom: '40px' }}>
          {t('documents.title')} {/* Usando tradução para "Documentos" */}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#555', textAlign: 'center', marginBottom: '40px' }}>
          {t('documents.subtitle')} {/* Usando tradução para o subtítulo */}
        </p>
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {documentos.map(documento => (
            <li key={documento.id} style={{ marginBottom: '30px', padding: '20px', borderBottom: '1px solid #ddd' }}>
              <Row>
                <Col md={8}>
                  <h5 style={{ fontWeight: 'bold', color: '#006400', marginBottom: '10px' }}>
                    {documento.title || t('documents.noTitleAvailable')} {/* Usando tradução para "Título não disponível" */}
                  </h5>
                  <p style={{ marginBottom: '15px', color: '#555' }}>
                    {documento.description || t('documents.noDescriptionAvailable')} {/* Usando tradução para "Descrição não disponível" */}
                  </p>
                </Col>
                <Col md={4} className="text-md-right">
                  <Button 
                    href={documento.file} 
                    variant="success" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    download
                    style={{ padding: '10px 20px', fontWeight: 'bold' }}
                  >
                    {t('documents.downloadButton')} {/* Usando tradução para "Baixar Documento" */}
                  </Button>
                </Col>
              </Row>
            </li>
          ))}
        </ul>
      </Container>
      <Footer />
    </div>
  );
}

export default Documentos;
