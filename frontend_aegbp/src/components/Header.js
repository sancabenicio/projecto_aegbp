import React, { useEffect } from 'react';
import { Navbar, Nav, NavDropdown, Container } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const Header = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();

  useEffect(() => {
    const path = window.location.pathname;
    const match = path.match(/^\/([a-z]{2})\//); // Verifica se há prefixo de idioma na URL

    if (!match) {
      // Detecta o idioma do navegador
      const browserLanguage = navigator.language.split('-')[0]; // Extrai o idioma principal (ex: 'pt' de 'pt-BR')
      const supportedLanguages = ['pt', 'en']; // Defina os idiomas suportados
      const defaultLanguage = supportedLanguages.includes(browserLanguage) ? browserLanguage : 'pt'; // Se não for suportado, use português

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

  // Função para alterar o idioma manualmente e redirecionar para a nova rota com o prefixo de idioma
  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    const pathWithoutLang = window.location.pathname.replace(/^\/[a-z]{2}\//, '/'); // Remove o prefixo do idioma atual da URL
    navigate(`/${lng}${pathWithoutLang}`, { replace: true });  // Redireciona para o novo idioma mantendo a mesma rota
  };

  return (
    <Navbar bg="light" expand="lg">
      <Container className="d-flex justify-content-between">
        <LinkContainer to={`/${i18n.language}/`}>
          <Navbar.Brand>
            <img
              src="/images/logo_AEGBP.png"
              alt="AEGB-Porto"
              width="40"
              height="40"
              className="d-inline-block align-top"
            />
            <span style={{ marginLeft: '10px', fontSize: '1.5rem', color: '#006400' }}>AEGB-Porto</span>
          </Navbar.Brand>
        </LinkContainer>
        <Navbar.Toggle aria-controls="navbarNav" />
        <Navbar.Collapse id="navbarNav" className="justify-content-end">
          <Nav>
            <LinkContainer to={`/${i18n.language}/`}>
              <Nav.Link style={{ marginRight: '10px' }}>{t('header.home', 'Home')}</Nav.Link>
            </LinkContainer>
            <LinkContainer to={`/${i18n.language}/sobre`}>
              <Nav.Link style={{ marginRight: '10px' }}>{t('header.about', 'Sobre')}</Nav.Link>
            </LinkContainer>
            <NavDropdown title={t('header.galleries', 'Galerias')} id="galerias-dropdown" style={{ marginRight: '10px' }}>
              <LinkContainer to={`/${i18n.language}/galeria-fotos`}>
                <NavDropdown.Item>{t('header.photoGallery', 'Galeria de Fotos')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/galeria-videos`}>
                <NavDropdown.Item>{t('header.videoGallery', 'Galeria de Vídeos')}</NavDropdown.Item>
              </LinkContainer>
            </NavDropdown>

            <NavDropdown title={t('header.resources', 'Recursos')} id="recursos-dropdown" style={{ marginRight: '10px' }}>
              <LinkContainer to={`/${i18n.language}/calendario`}>
                <NavDropdown.Item>{t('header.calendar', 'Calendário')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/documentos`}>
                <NavDropdown.Item>{t('header.documents', 'Documentos')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/blog`}>
                <NavDropdown.Item>{t('header.blog', 'Blog')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/depoimentos`}>
                <NavDropdown.Item>{t('header.testimonials', 'Depoimentos')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/faq`}>
                <NavDropdown.Item>{t('header.faq', 'Perguntas Frequentes')}</NavDropdown.Item>
              </LinkContainer>
            </NavDropdown>

            <NavDropdown title={t('header.getInvolved', 'Envolva-se')} id="envolva-se-dropdown" style={{ marginRight: '10px' }}>
              <LinkContainer to={`/${i18n.language}/voluntariado`}>
                <NavDropdown.Item>{t('header.volunteer', 'Oportunidades de Voluntariado')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/projetos`}>
                <NavDropdown.Item>{t('header.projects', 'Projetos')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/doacoes`}>
                <NavDropdown.Item>{t('header.donations', 'Doações')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/patrocinadores`}>
                <NavDropdown.Item>{t('header.sponsors', 'Patrocinadores')}</NavDropdown.Item>
              </LinkContainer>
              <LinkContainer to={`/${i18n.language}/membros`}>
                <NavDropdown.Item>{t('header.registerMember', 'Regista-se como Membro')}</NavDropdown.Item>
              </LinkContainer>
            </NavDropdown>

            <LinkContainer to={`/${i18n.language}/contatos`}>
              <Nav.Link style={{ marginRight: '10px' }}>{t('header.contacts', 'Contatos')}</Nav.Link>
            </LinkContainer>

            {/* Troca de idioma */}
            <NavDropdown title={i18n.language.toUpperCase()} id="language-dropdown">
              <NavDropdown.Item onClick={() => changeLanguage('pt')}>PT</NavDropdown.Item>
              <NavDropdown.Item onClick={() => changeLanguage('en')}>EN</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
