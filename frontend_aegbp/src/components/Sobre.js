import React, { useState, useEffect } from 'react';
import { Container, Spinner, Alert, Image, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const Sobre = ({ showFooter = true }) => {
  const { t, i18n } = useTranslation();
  const [aboutData, setAboutData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/about/`;

    axios.get(apiUrl)
      .then(response => {
        const data = response.data[0];
        setAboutData({
          title: data[`title_${i18n.language}`] || data.title,
          description: data[`description_${i18n.language}`] || data.description,
          image: data.image,
        });
        setLoading(false);
      })
      .catch(error => {
        console.error(t('sobre.errorLoading'), error);
        setError(t('sobre.errorLoadingMessage'));
        setLoading(false);
      });
  }, [t, i18n.language]);

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('sobre.loading')}</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  return (
    <Container className="py-5">
      <h1 style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700', textAlign: 'center' }}>
        {aboutData?.title || t('sobre.defaultTitle')}
      </h1>
      <Row className="align-items-center mt-5">
        <Col md={6}>
          <p style={{ fontWeight: '500', fontSize: '1.2rem', color: '#000', textAlign: 'left' }}>
            {aboutData?.description || t('sobre.defaultDescription')}
          </p>
        </Col>
        <Col md={6} className="text-center">
          {aboutData?.image && (
            <Image src={aboutData.image} alt={aboutData.title} fluid />
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default Sobre;
