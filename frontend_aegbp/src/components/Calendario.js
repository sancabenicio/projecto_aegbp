import React, { useState, useEffect } from 'react';
import { Container, Spinner, Alert, Row, Col } from 'react-bootstrap';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const Calendario = () => {
  const [eventos, setEventos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { t, i18n } = useTranslation(); // Inicializando o hook useTranslation e i18n para obter o idioma atual

  const getLanguagePrefix = () => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//);
    return match ? match[1] : 'en';
  };

  useEffect(() => {
    const languagePrefix = getLanguagePrefix();
    const apiUrl = `http://localhost:8000/${languagePrefix}/api/events/`;

    axios.get(apiUrl)
      .then(response => {
        const eventosTraduzidos = response.data.map(evento => ({
          ...evento,
          name: evento[`name_${i18n.language}`] || evento.name,
          description: evento[`description_${i18n.language}`] || evento.description,
        }));
        setEventos(eventosTraduzidos);
        setLoading(false);
      })
      .catch(error => {
        setError(t('calendar.errorLoading')); // Usando tradução para mensagens de erro
        setLoading(false);
      });
  }, [t, i18n.language]); // Adicionando i18n.language como dependência

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="sr-only">{t('calendar.loading')}</span> {/* Usando tradução para o texto de carregamento */}
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger" className="text-center">{error}</Alert>;
  }

  if (!eventos || eventos.length === 0) {
    return <p className="text-center">{t('calendar.noEventsFound')}</p>;
  }

  return (
    <div>
      <Container className="py-5">
        <h1 className="text-center" style={{ fontWeight: 'bold', fontSize: '3rem', color: '#FFD700' }}>
          {t('calendar.title')} {/* Usando tradução para "Eventos" */}
        </h1>
        <p className="text-center" style={{ fontWeight: '500', fontSize: '1.5rem', color: '#000' }}>
          {t('calendar.subtitle')} {/* Usando tradução para o subtítulo */}
        </p>
        <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
          {eventos.map(evento => (
            <li key={evento.id} style={{ marginBottom: '20px', padding: '15px', borderBottom: '1px solid #ddd' }}>
              <Row>
                <Col md={8}>
                  <h5 style={{ fontWeight: 'bold', color: '#333' }}>
                    {evento.name || t('calendar.noEventName')} {/* Usando tradução para "Nome do evento não disponível" */}
                  </h5>
                  <p style={{ margin: '0.5rem 0', color: '#555' }}>
                    <strong>{t('calendar.date')}:</strong> {evento.date || t('calendar.noDateAvailable')} {/* Usando tradução para "Data" */}
                  </p>
                  <p style={{ margin: '0.5rem 0', color: '#555' }}>
                    <strong>{t('calendar.time')}:</strong> {evento.start_time || t('calendar.noStartTimeAvailable')} - {evento.end_time || t('calendar.noEndTimeAvailable')} {/* Usando tradução para "Horário" */}
                  </p>
                </Col>
                <Col md={4} className="text-md-right">
                  <p style={{ margin: '0.5rem 0', color: '#555' }}>
                    {evento.description || t('calendar.noDescriptionAvailable')} {/* Usando tradução para "Descrição não disponível" */}
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

export default Calendario;
