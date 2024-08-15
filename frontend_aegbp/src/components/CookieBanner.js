import React, { useState, useEffect } from 'react';
import { Button, Container, Modal, Form } from 'react-bootstrap';
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const CookieBanner = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [showBanner, setShowBanner] = useState(false);
  const [showPreferences, setShowPreferences] = useState(false);
  const [preferences, setPreferences] = useState({
    essential: true, // Cookies essenciais devem ser marcados e obrigatórios
    analytics: false,
    marketing: false,
  });

  useEffect(() => {
    const consent = localStorage.getItem('cookieConsent');
    if (!consent) {
      setShowBanner(true);
    }
  }, []);

  const handleAcceptAll = () => {
    localStorage.setItem('cookieConsent', 'true');
    localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
    setShowBanner(false);
  };

  const handleRejectAll = () => {
    localStorage.setItem('cookieConsent', 'false');
    localStorage.setItem('cookiePreferences', JSON.stringify({ essential: true, analytics: false, marketing: false }));
    setShowBanner(false);
  };

  const handleSavePreferences = () => {
    localStorage.setItem('cookieConsent', 'true');
    localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
    setShowBanner(false);
    setShowPreferences(false);
  };

  const handleChangePreference = (event) => {
    const { name, checked } = event.target;
    setPreferences((prevPreferences) => ({
      ...prevPreferences,
      [name]: checked,
    }));
  };

  const openPreferences = () => {
    setShowPreferences(true);
  };

  const closePreferences = () => {
    setShowPreferences(false);
  };

  if (!showBanner) return null;

  return (
    <>
      <div style={{ position: 'fixed', bottom: 0, width: '100%', backgroundColor: '#343a40', color: '#fff', padding: '15px', zIndex: 1000 }}>
        <Container className="d-flex justify-content-between align-items-center flex-column flex-md-row">
          <p style={{ margin: 0, textAlign: 'center', fontSize: '14px' }}>
            {t('cookieBanner.message')}{' '}
            <button
              style={{ color: '#FFD700', textDecoration: 'underline', background: 'none', border: 'none', padding: 0, cursor: 'pointer' }}
              onClick={() => document.getElementById('privacy-link').click()}
            >
              {t('cookieBanner.privacyPolicy')}
            </button>.
          </p>
          <div className="d-flex justify-content-center mt-3 mt-md-0">
            <Button onClick={handleRejectAll} variant="warning" style={{ borderRadius: '20px', marginRight: '5px', padding: '4px 8px', fontSize: '12px' }}>
              {t('cookieBanner.reject')}
            </Button>
            <Button onClick={openPreferences} variant="warning" style={{ borderRadius: '20px', marginRight: '5px', padding: '4px 8px', fontSize: '12px' }}>
              {t('cookieBanner.managePreferences')}
            </Button>
            <Button onClick={handleAcceptAll} variant="warning" style={{ borderRadius: '20px', padding: '4px 8px', fontSize: '12px' }}>
              {t('cookieBanner.acceptAll')}
            </Button>
          </div>
        </Container>
      </div>

      <Modal show={showPreferences} onHide={closePreferences} centered>
        <Modal.Header closeButton>
          <Modal.Title>{t('cookieBanner.managePreferencesTitle')}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="essentialCookies">
              <Form.Check
                type="checkbox"
                label={t('cookieBanner.essentialCookies')}
                checked={preferences.essential}
                disabled
              />
              <Form.Text className="text-muted">{t('cookieBanner.essentialCookiesDescription')}</Form.Text>
            </Form.Group>

            <Form.Group controlId="analyticsCookies">
              <Form.Check
                type="checkbox"
                label={t('cookieBanner.analyticsCookies')}
                name="analytics"
                checked={preferences.analytics}
                onChange={handleChangePreference}
              />
              <Form.Text className="text-muted">{t('cookieBanner.analyticsCookiesDescription')}</Form.Text>
            </Form.Group>

            <Form.Group controlId="marketingCookies">
              <Form.Check
                type="checkbox"
                label={t('cookieBanner.marketingCookies')}
                name="marketing"
                checked={preferences.marketing}
                onChange={handleChangePreference}
              />
              <Form.Text className="text-muted">{t('cookieBanner.marketingCookiesDescription')}</Form.Text>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={closePreferences} style={{ fontSize: '12px', padding: '4px 8px' }}>
            {t('cookieBanner.cancel')}
          </Button>
          <Button variant="warning" onClick={handleSavePreferences} style={{ fontSize: '12px', padding: '4px 8px' }}>
            {t('cookieBanner.savePreferences')}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default CookieBanner;
