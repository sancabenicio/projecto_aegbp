import React, { useState, useRef, useCallback } from 'react';
import './Galeria.css';
import { Modal } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

const Galeria = ({ items, type }) => {
  const { t } = useTranslation();
  const [selectedItem, setSelectedItem] = useState(null);
  const [show, setShow] = useState(false);
  const modalRef = useRef(null);

  const openFullscreen = useCallback(() => {
    if (modalRef.current) {
      if (modalRef.current.requestFullscreen) {
        modalRef.current.requestFullscreen();
      } else if (modalRef.current.mozRequestFullScreen) { /* Firefox */
        modalRef.current.mozRequestFullScreen();
      } else if (modalRef.current.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
        modalRef.current.webkitRequestFullscreen();
      } else if (modalRef.current.msRequestFullscreen) { /* IE/Edge */
        modalRef.current.msRequestFullscreen();
      }
    }
  }, []);

  const exitFullscreen = useCallback(() => {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { /* Firefox */
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { /* Chrome, Safari & Opera */
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE/Edge */
      document.msExitFullscreen();
    }
  }, []);

  const handleShow = useCallback((item) => {
    setSelectedItem(item);
    setShow(true);
    openFullscreen();
  }, [openFullscreen]); // Adicionando a dependência 'openFullscreen'

  const handleClose = useCallback(() => {
    if (document.fullscreenElement) {
      exitFullscreen();
    }
    setShow(false);
  }, [exitFullscreen]); // Adicionando a dependência 'exitFullscreen'

  const extractVideoDetails = useCallback((item) => {
    const { link, file } = item;
    let embedUrl, thumbnailUrl;

    if (file) {
      embedUrl = file;
      thumbnailUrl = null;
    } else if (link && (link.includes('youtube.com') || link.includes('youtu.be'))) {
      const youtubeRegex = /(?:youtube\.com\/(?:[^/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
      const matches = link.match(youtubeRegex);
      const videoId = matches ? matches[1] : null;
      embedUrl = `https://www.youtube.com/embed/${videoId}`;
      thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
    } else if (link && link.includes('vimeo.com')) {
      const vimeoRegex = /vimeo\.com\/(\d+)/;
      const matches = link.match(vimeoRegex);
      const videoId = matches ? matches[1] : null;
      embedUrl = `https://player.vimeo.com/video/${videoId}`;
      thumbnailUrl = `https://vumbnail.com/${videoId}.jpg`;
    } else if (link && link.match(/\.(mp4|webm|ogg)$/)) {
      embedUrl = link;
      thumbnailUrl = null;
    } else {
      embedUrl = link;
      thumbnailUrl = null;
    }

    return { embedUrl, thumbnailUrl };
  }, []);

  return (
    <div>
      <div className="gallery-container">
        {items && Array.isArray(items) && items.length > 0 ? (
          items.map((item, index) => {
            const { embedUrl, thumbnailUrl } = extractVideoDetails(item);

            return (
              <div
                className="gallery-item"
                key={index}
                onClick={() => handleShow({ ...item, embedUrl })}
                style={{ cursor: 'pointer' }}
              >
                {type === 'video' ? (
                  <>
                    {thumbnailUrl ? (
                      <img 
                        src={thumbnailUrl} 
                        alt={item.title} 
                        className="gallery-image"
                      />
                    ) : (
                      <video className="gallery-image" controls>
                        <source src={embedUrl} type="video/mp4" />
                        {t('gallery.videoNotSupported')}
                      </video>
                    )}
                    <div className="gallery-overlay">
                      <h3>{item.title}</h3>
                      <p>{item.description}</p>
                    </div>
                  </>
                ) : (
                  <>
                    <img 
                      src={item.image} 
                      alt={item.caption} 
                      className="gallery-image" 
                    />
                    <div className="gallery-overlay">
                      <h3>{item.caption}</h3>
                    </div>
                  </>
                )}
              </div>
            );
          })
        ) : (
          <p>{t('gallery.noItemsFound')}</p>
        )}
      </div>

      <Modal
        show={show}
        onHide={handleClose}
        centered
        dialogClassName="fullscreen-modal"
      >
        <div ref={modalRef}>
          <Modal.Header closeButton>
            <Modal.Title>{type === 'video' ? selectedItem?.title : selectedItem?.caption}</Modal.Title>
          </Modal.Header>
          <Modal.Body style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {type === 'video' && selectedItem ? (
              selectedItem.file ? (
                <video controls style={{ maxWidth: '100%', maxHeight: '100vh' }}>
                  <source src={selectedItem.embedUrl} type="video/mp4" />
                  {t('gallery.videoNotSupported')}
                </video>
              ) : (
                <iframe
                  width="100%"
                  height="500px"
                  src={selectedItem.embedUrl}
                  title={selectedItem.title}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              )
            ) : (
              <img
                src={selectedItem?.image}
                alt={selectedItem?.caption}
                style={{ maxWidth: '100%', maxHeight: '100vh' }}
              />
            )}
          </Modal.Body>
        </div>
      </Modal>
    </div>
  );
};

export default Galeria;
