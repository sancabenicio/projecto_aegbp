import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Modal, Button } from 'react-bootstrap';
import axios from 'axios';
import { FaInstagram } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation

const Footer = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation
  const [privacyPolicy, setPrivacyPolicy] = useState('');
  const [socialLinks, setSocialLinks] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const currentYear = new Date().getFullYear();

  useEffect(() => {
    const fetchPrivacyPolicy = async () => {
      try {
        const response = await axios.get('http://localhost:8000/pt/api/Privacy/');
        if (response.data && response.data.length > 0) {
          setPrivacyPolicy(response.data[0].content);
        }
      } catch (error) {
        console.error(t('footer.errorFetchingPrivacyPolicy'), error); // Usando tradução para mensagens de erro
      }
    };

    const fetchSocialLinks = async () => {
      try {
        const response = await axios.get('http://localhost:8000/pt/api/Social/');
        setSocialLinks(response.data);
      } catch (error) {
        console.error(t('footer.errorFetchingSocialLinks'), error); // Usando tradução para mensagens de erro
      }
    };

    fetchPrivacyPolicy();
    fetchSocialLinks();
  }, [t]);

  const handleClose = () => {
    setShowModal(false);
  };

  const handleShow = () => setShowModal(true);

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([privacyPolicy], { type: 'text/html' });
    element.href = URL.createObjectURL(file);
    element.download = 'Politica_de_Privacidade.html';
    document.body.appendChild(element);
    element.click();
  };

  return (
    <footer style={{ backgroundColor: '#ffffff', padding: '30px 0', color: '#333', marginTop: '20px', borderTop: '1px solid #ddd' }}>
      <Container>
        <Row>
          <Col md={3} className="text-center text-md-left mb-4 mb-md-0">
            <h5 style={{ fontWeight: 'bold', color: '#006400' }}>{t('footer.aegbPorto')}</h5> {/* Usando tradução para "AEGB-Porto" */}
            <p style={{ margin: 0, color: '#555' }}>© {currentYear} {t('footer.allRightsReserved')}</p> {/* Usando tradução para "Todos os direitos reservados" */}
          </Col>
          <Col md={3} className="text-center text-md-left mb-4 mb-md-0">
            <h5 style={{ fontWeight: 'bold', color: '#006400' }}>{t('footer.quickLinks')}</h5> {/* Usando tradução para "Links Rápidos" */}
            <ul className="list-unstyled" style={{ margin: 0 }}>
              <li>
                <Link to="/" style={{ color: '#555', textDecoration: 'none' }}>{t('footer.home')}</Link> {/* Usando tradução para "Início" */}
              </li>
              <li>
                <Link to="/sobre" style={{ color: '#555', textDecoration: 'none' }}>{t('footer.aboutUs')}</Link> {/* Usando tradução para "Sobre Nós" */}
              </li>
              <li>
                <Link to="/projetos" style={{ color: '#555', textDecoration: 'none' }}>{t('footer.projects')}</Link> {/* Usando tradução para "Projetos" */}
              </li>
              <li>
                <Link to="/contatos" style={{ color: '#555', textDecoration: 'none' }}>{t('footer.contactUs')}</Link> {/* Usando tradução para "Contate-Nos" */}
              </li>
              <li>
                <Link to="#" id="privacy-link" onClick={handleShow} style={{ color: '#555', textDecoration: 'none' }}>{t('footer.privacyPolicy')}</Link> {/* Usando tradução para "Política de Privacidade" */}
              </li>
            </ul>
          </Col>
          <Col md={3} className="text-center text-md-left mb-4 mb-md-0">
            <h5 style={{ fontWeight: 'bold', color: '#006400' }}>{t('footer.information')}</h5> {/* Usando tradução para "Informações" */}
            <p style={{ margin: 0 }}>
              <Link to="#" onClick={handleShow} style={{ color: '#555', textDecoration: 'none' }}>
                {t('footer.privacyPolicy')}
              </Link>
            </p>
          </Col>
          <Col md={3} className="text-center text-md-left">
            <h5 style={{ fontWeight: 'bold', color: '#006400' }}>{t('footer.followUs')}</h5> {/* Usando tradução para "Siga-nos" */}
            {socialLinks.map((social) => (
              <a key={social.id} href={social.url} target="_blank" rel="noopener noreferrer" style={{ color: '#555', marginRight: '15px' }}>
                {social.platform === 'instagram' && <FaInstagram size={24} />}
              </a>
            ))}
          </Col>
        </Row>
      </Container>

      <Modal show={showModal} onHide={handleClose} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{t('footer.privacyPolicy')}</Modal.Title> {/* Usando tradução para "Política de Privacidade" */}
        </Modal.Header>
        <Modal.Body>
          <div dangerouslySetInnerHTML={{ __html: privacyPolicy }} />
          <div className="text-center mt-4">
            <Button variant="outline-success" onClick={handleDownload} style={{ padding: '10px 20px', fontWeight: 'bold' }}>
              {t('footer.downloadPrivacyPolicy')} {/* Usando tradução para "Descarregar Política de Privacidade" */}
            </Button>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            {t('footer.close')} {/* Usando tradução para "Fechar" */}
          </Button>
        </Modal.Footer>
      </Modal>
    </footer>
  );
};

export default Footer;
