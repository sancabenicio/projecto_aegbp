document.addEventListener('DOMContentLoaded', function () {
    // Atualiza o ano atual no rodapé
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    // Configurações de inatividade
    var idleTime = 0;
    const warningTime = 10; // Minutos de inatividade antes de avisar o usuário
    const logoutTime = 15; // Minutos de inatividade antes de desconectar o usuário

    // Incrementa o contador de inatividade a cada minuto
    setInterval(timerIncrement, 60000); // 1 minuto

    function timerIncrement() {
        idleTime++;
        if (idleTime >= warningTime) {
            alert("Você está inativo há algum tempo. Você será desconectado em breve se não houver nenhuma atividade.");
        }
        if (idleTime >= logoutTime) {
            window.location.href = logoutUrl;
        }
    }

    // Reseta o contador de inatividade ao detectar interação do usuário
    document.addEventListener('mousemove', resetIdleTime);
    document.addEventListener('keypress', resetIdleTime);

    function resetIdleTime() {
        idleTime = 0;
    }

    // Alternar entre modo claro e escuro
    function toggleTheme() {
        const body = document.body;
        const themeButton = document.getElementById('toggleTheme');
        body.classList.toggle('dark-mode');
        
        if (body.classList.contains('dark-mode')) {
            themeButton.classList.replace('fa-moon', 'fa-sun');
        } else {
            themeButton.classList.replace('fa-sun', 'fa-moon');
        }
    }

    // Detecta automaticamente o modo noturno baseado no horário
    function autoDetectTheme() {
        const hour = new Date().getHours();
        if (hour >= 19 || hour <= 7) {
            document.body.classList.add('dark-mode');
            document.getElementById('toggleTheme').classList.replace('fa-moon', 'fa-sun');
        }
    }

    document.getElementById('toggleTheme').addEventListener('click', toggleTheme);
    autoDetectTheme();

    // Inicializa dropdowns
    initializeDropdown('dropdown-toggle', 'dropdown-menu');
    initializeDropdown('languageDropdown', 'languageDropdownMenu');

    function initializeDropdown(toggleId, menuId) {
        const toggle = document.getElementById(toggleId);
        const menu = document.getElementById(menuId);

        if (toggle && menu) {
            toggle.addEventListener('click', () => {
                menu.classList.toggle('show');
            });

            document.addEventListener('click', function(event) {
                if (!toggle.contains(event.target) && !menu.contains(event.target)) {
                    menu.classList.remove('show');
                }
            });
        }
    }

    // Inicializa dropdown de notificações
    const notificationDropdownButton = document.getElementById('notificationDropdown');
    const notificationDropdownMenu = document.querySelector('.dropdown-menu[aria-labelledby="notificationDropdown"]');

    if (notificationDropdownButton && notificationDropdownMenu) {
        notificationDropdownButton.addEventListener('click', function(event) {
            event.stopPropagation();
            const isExpanded = notificationDropdownButton.getAttribute('aria-expanded') === 'true';
            notificationDropdownButton.setAttribute('aria-expanded', !isExpanded);
            notificationDropdownMenu.classList.toggle('show', !isExpanded);
        });

        document.addEventListener('click', function(event) {
            if (!notificationDropdownButton.contains(event.target) && !notificationDropdownMenu.contains(event.target)) {
                notificationDropdownButton.setAttribute('aria-expanded', 'false');
                notificationDropdownMenu.classList.remove('show');
            }
        });
    }

    // Inicializa itens de notificação
    initializeNotificationItems();

    function initializeNotificationItems() {
        const notificationItems = document.querySelectorAll('.notification-item');

        notificationItems.forEach(item => {
            item.addEventListener('click', function(event) {
                event.preventDefault();
                const id = this.getAttribute('data-id');
                const type = this.getAttribute('data-type');
                const url = `/view_notification/${type}/${id}/`;

                fetch(url, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const notificationCountElement = document.getElementById('notification-count');
                        if (notificationCountElement) {
                            notificationCountElement.textContent = data.total_notifications;
                            if (data.total_notifications == 0) {
                                notificationCountElement.style.display = 'none';
                            }
                        }
                        window.location.href = this.href;
                    } else {
                        console.error('Failed to mark notification as read');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        });
    }
});
