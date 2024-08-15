import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { useTranslation } from 'react-i18next'; // Importando o hook useTranslation
import Header from './Header';
import Footer from './Footer';
import Sobre from './Sobre';
import Blog from './Blog';
import Calendario from './Calendario';
import Depoimentos from './Depoimentos';
import Contatos from './Contatos';
import Divider from './Divider';
import CookieBanner from './CookieBanner';

const Home = () => {
  const { t } = useTranslation(); // Inicializando o hook useTranslation

  return (
    <div>
      <Header />
      <div
        className="container-fluid"
        style={{
          backgroundImage: 'url(/images/image.png)',
          backgroundSize: 'cover',
          height: '100vh',
          color: 'white',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center'
        }}
      >
        <h1 style={{ fontWeight: 'bold', fontSize: '3.4rem', color: '#FFD700' }}>
          {t('home.title', 'Associação de Estudantes da Guiné-Bissau no Porto')}
        </h1>
        <p style={{ fontWeight: '500', fontSize: '1.5rem', color: '#FFFFFF' }}>
          {t('home.subtitle', 'Sua plataforma para se envolver e conectar-se com a comunidade acadêmica')}
        </p>

        <Link to="/membros">
          <Button
            style={{
              marginTop: '20px',
              padding: '10px 30px',
              fontSize: '1.25rem',
              color: '#FFFFFF',
              border: '2px solid #FFFFFF',
              borderRadius: '30px',
              backgroundColor: 'transparent',
              fontWeight: 'bold'
            }}
          >
            {t('home.joinButton', 'Torna-se Membro')}
          </Button>
        </Link>
      </div>

      {/* Renderizar seções com divisores */}
      <Sobre />
      <Divider />
      <Blog />
      <Divider />
      <Calendario />
      <Divider />
      <Depoimentos />
      <Divider />
      <Contatos />

      <Footer />

      {/* Inclui o CookieBanner */}
      <CookieBanner />
    </div>
  );
}

export default Home;
