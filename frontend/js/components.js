// Componentes de la interfaz

const Components = {
    // Renderizar la aplicación completa
    renderApp(state) {
        if (!state.userType || state.currentPage === 'login') {
            return this.renderLogin();
        }

        return `
            ${this.renderNavbar(state)}
            <div class="min-h-screen">
                ${this.renderContent(state)}
            </div>
        `;
    },

    renderContent(state) {
        switch (state.currentPage) {
            case 'home':
                return this.renderClienteDashboard();
            case 'validation':
                return this.renderStaffDashboard();
            case 'eventos':
                return this.renderEventos();
            case 'detalle':
                return this.renderDetalleEvento(state);
            case 'carrito':
                return this.renderCarrito(state);
            case 'mis-compras':
                return this.renderMisCompras(state);
            default:
                return '';
        }
    },

    // Login Component
    renderLogin() {
        return `
            <div class="login-container">
                <div class="login-bg-effect login-bg-effect-1"></div>
                <div class="login-bg-effect login-bg-effect-2"></div>
                <div class="login-bg-effect login-bg-effect-3"></div>
                
                <div class="login-content">
                    <div class="login-header">
                        <div class="login-logo">
                            <i data-lucide="music-2" style="width: 64px; height: 64px; color: var(--color-primary);"></i>
                            <h1 class="login-title">ZENTRY</h1>
                        </div>
                        <p class="login-subtitle">Plataforma de Gestión de Entradas para Conciertos</p>
                    </div>

                    <div class="login-form-container">
                        <div class="text-center mb-6">
                            <div class="login-icon">
                                <i data-lucide="log-in" style="width: 32px; height: 32px; color: white;"></i>
                            </div>
                            <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Iniciar Sesión</h2>
                            <p style="font-size: 0.875rem; color: var(--color-text-muted);">Ingresa tus credenciales para continuar</p>
                        </div>

                        <form id="login-form">
                            <div class="form-group">
                                <label class="form-label" for="email">Correo electrónico</label>
                                <input type="email" id="email" class="input" placeholder="correo@ejemplo.com" required>
                            </div>

                            <div class="form-group">
                                <label class="form-label" for="password">Contraseña</label>
                                <input type="password" id="password" class="input" placeholder="••••••••" required>
                            </div>

                            <div id="error-container"></div>

                            <button type="submit" class="btn btn-primary w-full" style="padding: 1rem;">
                                Iniciar sesión
                            </button>

                            <div class="text-center" style="margin-top: 1rem;">
                                <p style="font-size: 0.875rem; color: var(--color-text-muted);">
                                    ¿No tienes cuenta? 
                                    <a href="#" style="color: var(--color-primary);">Regístrate aquí</a>
                                </p>
                            </div>
                        </form>

                        <div class="credentials-demo">
                            <p style="font-size: 0.75rem; color: var(--color-text-muted); text-align: center; margin-bottom: 0.75rem;">
                                Credenciales de prueba:
                            </p>

                            <div class="credential-card">
                                <div class="credential-header">
                                    <div class="credential-icon">
                                        <i data-lucide="user" style="width: 12px; height: 12px; color: white;"></i>
                                    </div>
                                    <span class="credential-type">CLIENTE</span>
                                </div>
                                <div class="credential-details">
                                    <p><span style="color: var(--color-text-muted);">Email:</span> cliente@zentry.com</p>
                                    <p><span style="color: var(--color-text-muted);">Contraseña:</span> Zentry123</p>
                                </div>
                            </div>

                            <div class="credential-card" style="border-color: rgba(139, 92, 246, 0.3);">
                                <div class="credential-header">
                                    <div class="credential-icon" style="background: linear-gradient(135deg, var(--color-secondary) 0%, #a78bfa 100%);">
                                        <i data-lucide="shield" style="width: 12px; height: 12px; color: white;"></i>
                                    </div>
                                    <span class="credential-type" style="color: var(--color-secondary);">STAFF</span>
                                </div>
                                <div class="credential-details">
                                    <p><span style="color: var(--color-text-muted);">Email:</span> staff@zentry.com</p>
                                    <p><span style="color: var(--color-text-muted);">Contraseña:</span> Access2025</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <p style="text-align: center; color: var(--color-text-muted); font-size: 0.875rem; margin-top: 1.5rem;">
                        El sistema identificará automáticamente tu rol
                    </p>
                </div>
            </div>
        `;
    },

    // Navbar Component
    renderNavbar(state) {
        const isClient = state.userType === 'client';
        
        return `
            <nav class="navbar">
                <div class="navbar-content">
                    <div class="navbar-logo" onclick="AppState.navigate(${isClient ? "'home'" : "'validation'"})">
                        <i data-lucide="music-2" style="width: 32px; height: 32px; color: var(--color-primary);"></i>
                        <span class="navbar-brand">ZENTRY</span>
                    </div>

                    ${isClient ? `
                        <div class="navbar-links">
                            <div class="navbar-link ${state.currentPage === 'home' ? 'active' : ''}" onclick="AppState.navigate('home')">
                                <i data-lucide="home" style="width: 16px; height: 16px;"></i>
                                Inicio
                            </div>
                            <div class="navbar-link ${state.currentPage === 'eventos' || state.currentPage === 'detalle' ? 'active' : ''}" onclick="AppState.navigate('eventos')">
                                <i data-lucide="calendar" style="width: 16px; height: 16px;"></i>
                                Eventos
                            </div>
                            <div class="navbar-link ${state.currentPage === 'carrito' ? 'active' : ''}" onclick="AppState.navigate('carrito')">
                                <i data-lucide="shopping-cart" style="width: 16px; height: 16px;"></i>
                                Carrito
                                ${state.cartItems.length > 0 ? `<span class="cart-badge">${state.cartItems.length}</span>` : ''}
                            </div>
                            <div class="navbar-link ${state.currentPage === 'mis-compras' ? 'active' : ''}" onclick="AppState.navigate('mis-compras')">
                                <i data-lucide="ticket" style="width: 16px; height: 16px;"></i>
                                Mis Compras
                            </div>
                        </div>
                    ` : `
                        <div class="flex items-center gap-2">
                            <i data-lucide="shield" style="width: 20px; height: 20px; color: var(--color-secondary);"></i>
                            <span style="color: var(--color-text-secondary);">Panel de Validación</span>
                        </div>
                    `}

                    <button class="btn btn-outline" onclick="AppState.logout()">
                        <i data-lucide="log-out" style="width: 16px; height: 16px;"></i>
                        Cerrar sesión
                    </button>
                </div>
            </nav>
        `;
    },

    // Cliente Dashboard Component
    renderClienteDashboard() {
        return `
            <div class="dashboard-container">
                <div class="container">
                    <div class="hero-section">
                        <img src="https://images.unsplash.com/photo-1709731191876-899e32264420?w=1080&q=80" 
                             alt="Concierto" class="hero-image">
                        <div class="hero-overlay">
                            <div class="hero-content">
                                <div class="hero-badge">
                                    <i data-lucide="sparkles" style="width: 24px; height: 24px; color: var(--color-secondary);"></i>
                                    <span class="hero-badge-text">BIENVENIDO A ZENTRY</span>
                                </div>
                                <h1 class="hero-title">Vive la música en vivo</h1>
                                <p class="hero-description">
                                    Descubre los mejores conciertos y eventos musicales. Reserva tus entradas de forma segura y rápida.
                                </p>
                                <button class="btn btn-primary" style="padding: 1.5rem 2rem; font-size: 1.125rem;" onclick="AppState.navigate('eventos')">
                                    Explorar Eventos
                                    <i data-lucide="arrow-right" style="width: 20px; height: 20px;"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="grid md:grid-cols-3 mb-8">
                        <div class="card quick-action-card" onclick="AppState.navigate('eventos')">
                            <div class="quick-action-icon">
                                <i data-lucide="calendar" style="width: 24px; height: 24px; color: white;"></i>
                            </div>
                            <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem;">Catálogo de Eventos</h3>
                            <p style="color: var(--color-text-muted); margin-bottom: 1rem;">Explora nuestra selección de conciertos y eventos musicales</p>
                            <div style="display: flex; align-items: center; color: var(--color-primary); font-size: 0.875rem;">
                                <span style="margin-right: 0.5rem;">Ver eventos</span>
                                <i data-lucide="arrow-right" style="width: 16px; height: 16px;"></i>
                            </div>
                        </div>

                        <div class="card quick-action-card" onclick="AppState.navigate('carrito')">
                            <div class="quick-action-icon" style="background: linear-gradient(135deg, var(--color-secondary) 0%, #a78bfa 100%);">
                                <i data-lucide="shopping-bag" style="width: 24px; height: 24px; color: white;"></i>
                            </div>
                            <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem;">Mi Carrito</h3>
                            <p style="color: var(--color-text-muted); margin-bottom: 1rem;">Revisa tus entradas seleccionadas antes de comprar</p>
                            <div style="display: flex; align-items: center; color: var(--color-secondary); font-size: 0.875rem;">
                                <span style="margin-right: 0.5rem;">Ver carrito</span>
                                <i data-lucide="arrow-right" style="width: 16px; height: 16px;"></i>
                            </div>
                        </div>

                        <div class="card quick-action-card" onclick="AppState.navigate('mis-compras')">
                            <div class="quick-action-icon" style="background: linear-gradient(135deg, #4f46e5 0%, var(--color-primary) 100%);">
                                <i data-lucide="sparkles" style="width: 24px; height: 24px; color: white;"></i>
                            </div>
                            <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem;">Mis Compras</h3>
                            <p style="color: var(--color-text-muted); margin-bottom: 1rem;">Accede a tus tickets y descárgalos en PDF</p>
                            <div style="display: flex; align-items: center; color: #4f46e5; font-size: 0.875rem;">
                                <span style="margin-right: 0.5rem;">Ver compras</span>
                                <i data-lucide="arrow-right" style="width: 16px; height: 16px;"></i>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                            <div>
                                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Eventos Destacados</h2>
                                <p style="color: var(--color-text-muted);">Los conciertos más esperados del mes</p>
                            </div>
                            <button class="btn btn-outline" onclick="AppState.navigate('eventos')">
                                Ver todos
                                <i data-lucide="arrow-right" style="width: 16px; height: 16px;"></i>
                            </button>
                        </div>

                        <div class="grid md:grid-cols-2">
                            ${this.renderFeaturedEvents()}
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    renderFeaturedEvents() {
        const featured = AppState.events.filter(e => e.popular).slice(0, 2);
        return featured.map(event => `
            <div class="card event-card" style="padding: 0; cursor: pointer;" onclick="AppState.navigate('detalle', ${event.id})">
                <div class="event-image-container">
                    <img src="${event.image}" alt="${event.name}" class="event-image">
                    <div class="event-badge">Próximamente</div>
                </div>
                <div class="event-content">
                    <h3 style="font-size: 1.125rem; margin-bottom: 0.5rem;">${event.name}</h3>
                    <p style="font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: 0.75rem;">
                        ${event.date} • ${event.venue}
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: var(--color-primary);">Desde ${formatPrice(event.price)}</span>
                        <span style="font-size: 0.875rem; color: var(--color-text-muted);">${event.available} entradas disponibles</span>
                    </div>
                </div>
            </div>
        `).join('');
    },

    // Eventos Component
    renderEventos() {
        return `
            <div class="dashboard-container">
                <div class="container">
                    <div class="mb-8">
                        <h1 style="font-size: 2.25rem; font-weight: 700; margin-bottom: 0.5rem;">Catálogo de Eventos</h1>
                        <p style="color: var(--color-text-muted);">Descubre los mejores conciertos y eventos musicales</p>
                    </div>

                    <div class="card filters-container">
                        <div class="filters-header">
                            <i data-lucide="filter" style="width: 20px; height: 20px; color: var(--color-primary);"></i>
                            <h3>Filtros y Ordenamiento</h3>
                        </div>
                        <div class="filters-grid">
                            <div class="filter-group">
                                <label class="filter-label">Categoría</label>
                                <select id="filter-category" class="select" onchange="updateEventFilters()">
                                    <option value="all">Todas las categorías</option>
                                    <option value="electronica">Electrónica</option>
                                    <option value="rock">Rock</option>
                                    <option value="jazz">Jazz</option>
                                    <option value="pop">Pop</option>
                                    <option value="indie">Indie</option>
                                </select>
                            </div>
                            <div class="filter-group">
                                <label class="filter-label">Ordenar por</label>
                                <select id="sort-by" class="select" onchange="updateEventFilters()">
                                    <option value="date">Fecha</option>
                                    <option value="price-low">Precio: Menor a Mayor</option>
                                    <option value="price-high">Precio: Mayor a Menor</option>
                                    <option value="popular">Popularidad</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div id="events-grid" class="grid lg:grid-cols-3">
                        ${this.renderEventCards()}
                    </div>
                </div>
            </div>
        `;
    },

    renderEventCards(filterCategory = 'all', sortBy = 'date') {
        let events = [...AppState.events];

        // Filtrar
        if (filterCategory !== 'all') {
            events = events.filter(e => e.category === filterCategory);
        }

        // Ordenar
        if (sortBy === 'price-low') {
            events.sort((a, b) => a.price - b.price);
        } else if (sortBy === 'price-high') {
            events.sort((a, b) => b.price - a.price);
        } else if (sortBy === 'popular') {
            events.sort((a, b) => (b.popular ? 1 : 0) - (a.popular ? 1 : 0));
        }

        if (events.length === 0) {
            return '<div class="empty-state"><p style="color: var(--color-text-muted); font-size: 1.125rem;">No se encontraron eventos con los filtros seleccionados</p></div>';
        }

        return events.map(event => `
            <div class="card event-card" style="padding: 0;" onclick="AppState.navigate('detalle', ${event.id})">
                <div class="event-image-container">
                    <img src="${event.image}" alt="${event.name}" class="event-image">
                    ${event.popular ? '<div class="event-badge">Popular</div>' : ''}
                    <div style="position: absolute; inset: 0; background: linear-gradient(to top, var(--color-bg-secondary) 0%, transparent 50%); opacity: 0.6;"></div>
                </div>
                <div class="event-content">
                    <h3 class="event-title">${event.name}</h3>
                    <div class="event-details">
                        <i data-lucide="calendar" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                        ${event.date}
                    </div>
                    <div class="event-details">
                        <i data-lucide="map-pin" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                        ${event.venue}
                    </div>
                    <div class="event-footer">
                        <div>
                            <div class="event-price">
                                <i data-lucide="dollar-sign" style="width: 16px; height: 16px;"></i>
                                ${event.price.toFixed(2)}
                            </div>
                            <div class="event-available">
                                <i data-lucide="users" style="width: 12px; height: 12px;"></i>
                                ${event.available} disponibles
                            </div>
                        </div>
                        <button class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.875rem;">
                            Ver Detalles
                            <i data-lucide="arrow-right" style="width: 16px; height: 16px;"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    },

    // Detalle Evento Component
    renderDetalleEvento(state) {
        const event = state.eventData[state.selectedEventId];
        if (!event) return '<div>Evento no encontrado</div>';

        const seats = this.generateSeats(state.selectedEventId);
        const eventImage = AppState.events.find(e => e.id === state.selectedEventId)?.image || '';

        return `
            <div class="dashboard-container">
                <div class="container">
                    <button class="btn btn-ghost mb-6" onclick="AppState.navigate('eventos')">
                        <i data-lucide="arrow-left" style="width: 16px; height: 16px;"></i>
                        Volver a Eventos
                    </button>

                    <div class="seat-selection-layout">
                        <div>
                            <div style="border-radius: 0.75rem; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); margin-bottom: 1rem;">
                                <img src="${eventImage}" alt="${event.name}" style="width: 100%; height: 280px; object-fit: cover;">
                            </div>

                            <div class="card mb-4">
                                <h1 style="font-size: 1.875rem; font-weight: 700; margin-bottom: 0.75rem;">${event.name}</h1>
                                <p style="font-size: 0.875rem; color: var(--color-text-secondary); margin-bottom: 1rem;">
                                    El festival de música electrónica más grande del año. Disfruta de los mejores DJs internacionales en una experiencia inolvidable.
                                </p>

                                <div style="margin-bottom: 1rem;">
                                    <div class="event-details mb-2">
                                        <i data-lucide="calendar" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                        ${event.date}
                                    </div>
                                    <div class="event-details mb-2">
                                        <i data-lucide="clock" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                        ${event.time}
                                    </div>
                                    <div class="event-details">
                                        <i data-lucide="map-pin" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                        ${event.venue}
                                    </div>
                                </div>

                                <div style="border-top: 1px solid rgba(107, 114, 128, 0.5); padding-top: 1rem;">
                                    <h3 style="font-size: 0.875rem; margin-bottom: 0.5rem;">Zonas y Precios</h3>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.375rem; font-size: 0.875rem;">
                                        <div style="display: flex; align-items: center;">
                                            <div style="width: 12px; height: 12px; border-radius: 0.25rem; background: var(--color-secondary); margin-right: 0.5rem;"></div>
                                            <span style="color: var(--color-text-secondary);">VIP</span>
                                        </div>
                                        <span style="color: var(--color-secondary);">$120.00</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.375rem; font-size: 0.875rem;">
                                        <div style="display: flex; align-items: center;">
                                            <div style="width: 12px; height: 12px; border-radius: 0.25rem; background: var(--color-primary); margin-right: 0.5rem;"></div>
                                            <span style="color: var(--color-text-secondary);">Preferencial</span>
                                        </div>
                                        <span style="color: var(--color-primary);">$75.00</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.875rem;">
                                        <div style="display: flex; align-items: center;">
                                            <div style="width: 12px; height: 12px; border-radius: 0.25rem; background: #4f46e5; margin-right: 0.5rem;"></div>
                                            <span style="color: var(--color-text-secondary);">General</span>
                                        </div>
                                        <span style="color: #4f46e5;">$45.00</span>
                                    </div>
                                </div>
                            </div>

                            <div class="card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%); border-color: rgba(99, 102, 241, 0.5);">
                                <h3 style="margin-bottom: 1rem;">RESUMEN</h3>
                                <div style="display: flex; align-items: center; color: var(--color-text-secondary); margin-bottom: 0.75rem;">
                                    <i data-lucide="users" style="width: 20px; height: 20px; margin-right: 0.75rem; color: var(--color-primary);"></i>
                                    <span id="summary-seats-count">0 asientos reservados</span>
                                </div>
                                <div id="summary-actions"></div>
                            </div>
                        </div>

                        <div class="card">
                            <div style="margin-bottom: 1.5rem;">
                                <h2 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Selección de Asientos</h2>
                                <p style="color: var(--color-text-muted);">Haz clic en los asientos para seleccionar</p>
                            </div>

                            <div class="seat-legend">
                                <div class="seat-legend-item">
                                    <div class="seat-legend-box seat-legend-available"></div>
                                    <span style="color: var(--color-text-muted);">Disponible</span>
                                </div>
                                <div class="seat-legend-item">
                                    <div class="seat-legend-box seat-legend-selected"></div>
                                    <span style="color: var(--color-text-muted);">Seleccionado</span>
                                </div>
                                <div class="seat-legend-item">
                                    <div class="seat-legend-box seat-legend-occupied"></div>
                                    <span style="color: var(--color-text-muted);">Ocupado</span>
                                </div>
                            </div>

                            <div class="stage">ESCENARIO</div>

                            <div id="seats-container">
                                ${this.renderSeats(seats, state)}
                            </div>
                        </div>
                    </div>

                    <div id="floating-summary"></div>
                </div>
            </div>
        `;
    },

    generateSeats(eventId) {
        // Si ya existen asientos generados para este evento, retornarlos
        if (AppState.generatedSeats[eventId]) {
            return AppState.generatedSeats[eventId];
        }

        const seats = [];
        const zones = [
            { zone: "VIP", rows: 3, seatsPerRow: 8, price: 120 },
            { zone: "Preferencial", rows: 5, seatsPerRow: 10, price: 75 },
            { zone: "General", rows: 8, seatsPerRow: 12, price: 45 }
        ];

        let rowCounter = 1;
        zones.forEach(zoneConfig => {
            for (let r = 0; r < zoneConfig.rows; r++) {
                for (let s = 1; s <= zoneConfig.seatsPerRow; s++) {
                    // Usar un seed basado en el eventId y posición para generar disponibilidad consistente
                    const seed = eventId * 1000 + rowCounter * 100 + s;
                    const pseudoRandom = Math.sin(seed) * 10000;
                    const available = (pseudoRandom - Math.floor(pseudoRandom)) > 0.3; // 70% disponibles
                    
                    seats.push({
                        id: `${zoneConfig.zone}-R${rowCounter}-S${s}`,
                        row: rowCounter,
                        number: s,
                        zone: zoneConfig.zone,
                        price: zoneConfig.price,
                        available: available
                    });
                }
                rowCounter++;
            }
        });

        // Guardar los asientos generados en el estado global
        AppState.generatedSeats[eventId] = seats;
        return seats;
    },

    renderSeats(seats, state) {
        const zones = ["VIP", "Preferencial", "General"];
        
        return zones.map(zone => {
            const zoneSeats = seats.filter(s => s.zone === zone);
            const rows = [...new Set(zoneSeats.map(s => s.row))];
            const availableCount = zoneSeats.filter(s => s.available && !state.reservedSeats.has(s.id)).length;

            const zoneColors = {
                "VIP": "var(--color-secondary)",
                "Preferencial": "var(--color-primary)",
                "General": "#4f46e5"
            };

            return `
                <div class="zone-section">
                    <div class="zone-header">
                        <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: ${zoneColors[zone]}; border: 1px solid ${zoneColors[zone]};">
                            ${zone}
                        </span>
                        <span style="font-size: 0.875rem; color: var(--color-text-muted);">
                            ${availableCount} asientos disponibles
                        </span>
                    </div>
                    <div>
                        ${rows.map(row => {
                            const rowSeats = zoneSeats.filter(s => s.row === row);
                            return `
                                <div class="seat-row">
                                    <span class="seat-row-label">F${row}</span>
                                    ${rowSeats.map(seat => {
                                        const isInCart = state.reservedSeats.has(seat.id);
                                        const isAvailable = seat.available && !isInCart;
                                        const seatClass = isInCart ? 'occupied' : (!seat.available ? 'occupied' : '');
                                        
                                        return `
                                            <button 
                                                class="seat ${seatClass}" 
                                                data-seat-id="${seat.id}"
                                                data-seat-zone="${seat.zone}"
                                                data-seat-price="${seat.price}"
                                                ${!isAvailable ? 'disabled' : ''}
                                                onclick="toggleSeat('${seat.id}', '${seat.zone}', ${seat.price}, ${seat.row}, ${seat.number})"
                                            >
                                                ${seat.number}
                                            </button>
                                        `;
                                    }).join('')}
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }).join('');
    },

    // Carrito Component
    renderCarrito(state) {
        const total = state.cartItems.reduce((sum, item) => sum + item.price, 0);
        const serviceFee = total * 0.1;
        const grandTotal = total + serviceFee;

        return `
            <div class="dashboard-container">
                <div class="container">
                    <div class="mb-8" style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1 style="font-size: 2.25rem; font-weight: 700; margin-bottom: 0.5rem;">Mi Carrito</h1>
                            <p style="color: var(--color-text-muted);">
                                ${state.cartItems.length} ${state.cartItems.length === 1 ? 'entrada' : 'entradas'} en tu carrito
                            </p>
                        </div>
                        ${state.cartHistory.length > 0 ? `
                            <button class="btn btn-outline" onclick="AppState.undo()">
                                <i data-lucide="undo" style="width: 16px; height: 16px;"></i>
                                Deshacer última acción
                            </button>
                        ` : ''}
                    </div>

                    <div class="cart-items-container">
                        <div>
                            ${state.cartItems.length === 0 ? `
                                <div class="card empty-state">
                                    <i data-lucide="shopping-bag" class="empty-state-icon"></i>
                                    <h3 class="empty-state-title">Tu carrito está vacío</h3>
                                    <p class="empty-state-description">Explora nuestros eventos y agrega tus entradas favoritas</p>
                                </div>
                            ` : state.cartItems.map(item => `
                                <div class="card cart-item">
                                    <div class="cart-item-content">
                                        <h3 class="cart-item-title">${item.eventName}</h3>
                                        <div style="margin-bottom: 1rem;">
                                            <div class="event-details mb-2">
                                                <i data-lucide="calendar" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                                ${item.eventDate}
                                            </div>
                                            <div class="event-details">
                                                <i data-lucide="map-pin" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                                ${item.eventVenue}
                                            </div>
                                        </div>
                                        <div class="cart-item-details">
                                            <div class="cart-item-badge">
                                                <span style="color: var(--color-text-muted);">Zona: </span>
                                                <span style="color: var(--color-primary);">${item.zone}</span>
                                            </div>
                                            <div class="cart-item-badge">
                                                <span style="color: var(--color-text-muted);">Asiento: </span>
                                                <span>${item.seatId}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="cart-item-actions">
                                        <p class="cart-item-price">${formatPrice(item.price)}</p>
                                        <button class="btn btn-danger" onclick="AppState.removeItem('${item.id}')">
                                            <i data-lucide="trash-2" style="width: 16px; height: 16px;"></i>
                                            Eliminar
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>

                        <div class="order-summary">
                            <div class="card">
                                <h3 style="font-size: 1.25rem; margin-bottom: 1.5rem;">Resumen del Pedido</h3>

                                ${state.timerActive && state.cartItems.length > 0 ? `
                                    <div class="timer-box ${state.timeRemaining <= 60 ? 'warning' : 'normal'}">
                                        <p class="timer-label">Tiempo restante para completar tu compra</p>
                                        <p class="timer-value ${state.timeRemaining <= 60 ? 'warning' : 'normal'}">
                                            ${formatTime(state.timeRemaining)}
                                        </p>
                                    </div>
                                ` : ''}

                                <div style="margin-bottom: 1.5rem;">
                                    <div class="summary-line">
                                        <span>Subtotal (${state.cartItems.length} ${state.cartItems.length === 1 ? 'entrada' : 'entradas'})</span>
                                        <span>${formatPrice(total)}</span>
                                    </div>
                                    <div class="summary-line">
                                        <span>Cargo por servicio</span>
                                        <span>${formatPrice(serviceFee)}</span>
                                    </div>
                                    <div class="summary-total">
                                        <span class="summary-total-label">Total</span>
                                        <span class="summary-total-value">${formatPrice(grandTotal)}</span>
                                    </div>
                                </div>

                                <button 
                                    class="btn btn-primary w-full" 
                                    style="padding: 1.5rem; font-size: 1.125rem;"
                                    ${state.cartItems.length === 0 ? 'disabled' : ''}
                                    onclick="AppState.checkout()"
                                >
                                    <i data-lucide="credit-card" style="width: 20px; height: 20px;"></i>
                                    Proceder al Pago
                                </button>

                                <div class="summary-features">
                                    <p class="summary-feature">✓ Pago seguro y encriptado</p>
                                    <p class="summary-feature">✓ Tickets enviados por correo electrónico</p>
                                    <p class="summary-feature">✓ Cancelación hasta 48h antes del evento</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    // Mis Compras Component
    renderMisCompras(state) {
        return `
            <div class="dashboard-container">
                <div class="container">
                    <div class="mb-8">
                        <h1 style="font-size: 2.25rem; font-weight: 700; margin-bottom: 0.5rem;">Mis Compras</h1>
                        <p style="color: var(--color-text-muted);">Historial de tus entradas adquiridas</p>
                    </div>

                    ${state.purchases.length === 0 ? `
                        <div class="card empty-state">
                            <i data-lucide="ticket" class="empty-state-icon"></i>
                            <h3 class="empty-state-title">No tienes compras aún</h3>
                            <p class="empty-state-description">Tus tickets aparecerán aquí después de realizar una compra</p>
                        </div>
                    ` : state.purchases.map(purchase => `
                        <div class="card purchase-card">
                            <div class="purchase-header">
                                <div class="purchase-title-container">
                                    <div class="purchase-title-row">
                                        <h2 class="purchase-title">${purchase.eventName}</h2>
                                        <span class="badge badge-success">
                                            <i data-lucide="check-circle" style="width: 12px; height: 12px;"></i>
                                            Confirmado
                                        </span>
                                    </div>

                                    <div class="purchase-details-grid">
                                        <div class="event-details">
                                            <i data-lucide="calendar" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                            Evento: ${purchase.eventDate}
                                        </div>
                                        <div class="event-details">
                                            <i data-lucide="map-pin" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                                            ${purchase.eventVenue}
                                        </div>
                                    </div>

                                    <div class="purchase-date">
                                        Comprado el: ${purchase.purchaseDate}
                                    </div>
                                </div>

                                <button class="btn btn-primary" onclick="toast.success('Descargando ticket: ${purchase.eventName}')">
                                    <i data-lucide="download" style="width: 16px; height: 16px;"></i>
                                    Descargar PDF
                                </button>
                            </div>

                            <div class="seats-details">
                                <h4 class="seats-details-title">Detalles de las Entradas</h4>
                                <div class="seats-grid">
                                    ${purchase.seats.map(seat => `
                                        <div class="seat-detail-card">
                                            <div class="seat-detail-row">
                                                <span class="seat-detail-label">Asiento</span>
                                                <span class="seat-detail-value">${seat.seatId}</span>
                                            </div>
                                            <div class="seat-detail-row" style="margin-bottom: 0;">
                                                <span class="badge badge-primary">${seat.zone}</span>
                                                <span style="font-size: 0.875rem; color: var(--color-text-muted);">${formatPrice(seat.price)}</span>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>

                                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(107, 114, 128, 0.5);">
                                    <span style="color: var(--color-text-muted);">Total pagado</span>
                                    <span style="font-size: 1.25rem; font-weight: 700; color: var(--color-primary);">
                                        ${formatPrice(purchase.total)}
                                    </span>
                                </div>
                            </div>

                            <div class="qr-section">
                                <div class="qr-content">
                                    <div class="qr-placeholder">QR</div>
                                    <div>
                                        <p class="qr-info-label">Código de verificación</p>
                                        <p class="qr-code">${purchase.qrCode}</p>
                                    </div>
                                </div>
                                <p class="qr-description">
                                    Presenta este código QR al personal en la entrada del evento
                                </p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    // Staff Dashboard Component
    renderStaffDashboard() {
        return `
            <div class="dashboard-container">
                <div class="container" style="max-width: 64rem;">
                    <div class="staff-header">
                        <div class="staff-icon-container">
                            <i data-lucide="shield" style="width: 32px; height: 32px; color: white;"></i>
                        </div>
                        <h1 style="font-size: 2.25rem; font-weight: 700; margin-bottom: 0.5rem;">Panel de Validación</h1>
                        <p style="color: var(--color-text-muted);">Escanea o ingresa el código QR del ticket para validar</p>
                    </div>

                    <div class="card validation-form">
                        <form id="validation-form" onsubmit="handleValidation(event)">
                            <div class="form-group">
                                <label class="form-label" style="font-size: 1.125rem;">Código de Ticket</label>
                                <div class="input-with-icon">
                                    <input 
                                        type="text" 
                                        id="ticket-code" 
                                        class="input" 
                                        style="padding: 1.5rem 3rem 1.5rem 1rem; font-size: 1.125rem;"
                                        placeholder="Ingresa o escanea el código QR" 
                                        required
                                    >
                                    <i data-lucide="scan" class="input-icon" style="width: 24px; height: 24px;"></i>
                                </div>
                            </div>

                            <div class="form-actions">
                                <button type="submit" class="btn btn-primary" style="padding: 1.5rem; font-size: 1.125rem; background: linear-gradient(135deg, var(--color-secondary) 0%, #a78bfa 100%);">
                                    Validar Ticket
                                </button>
                                <button type="button" class="btn btn-outline" style="padding: 1.5rem;" onclick="resetValidation()">
                                    Limpiar
                                </button>
                            </div>
                        </form>

                        <div class="helper-codes">
                            <p style="font-size: 0.75rem; color: var(--color-text-muted); text-align: center; margin-bottom: 0.5rem;">
                                Códigos de prueba:
                            </p>
                            <div class="helper-codes-grid">
                                <div class="helper-code" style="color: var(--color-success);">VALID-12345</div>
                                <div class="helper-code" style="color: var(--color-warning);">USED-67890</div>
                                <div class="helper-code" style="color: var(--color-error);">INVALID-00000</div>
                            </div>
                        </div>
                    </div>

                    <div id="validation-result"></div>

                    <div class="stats-grid">
                        <div class="card stat-card">
                            <div class="stat-value success">248</div>
                            <p class="stat-label">Validados Hoy</p>
                        </div>
                        <div class="card stat-card">
                            <div class="stat-value warning">12</div>
                            <p class="stat-label">Duplicados</p>
                        </div>
                        <div class="card stat-card">
                            <div class="stat-value error">3</div>
                            <p class="stat-label">Rechazados</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    renderValidationResult(result) {
        if (!result) return '';

        const statusConfig = {
            valid: {
                class: 'valid',
                icon: 'check-circle',
                title: '✅ Ticket Válido',
                message: '✓ Permitir el acceso al evento',
                color: '#34d399'
            },
            used: {
                class: 'used',
                icon: 'alert-triangle',
                title: '⚠️ Ticket Ya Usado',
                message: '⚠ Este ticket ya fue validado anteriormente',
                color: '#fbbf24'
            },
            invalid: {
                class: 'invalid',
                icon: 'x-circle',
                title: '❌ Ticket Inválido',
                message: '❌ Este código no existe en el sistema. Denegar acceso.',
                color: '#f87171'
            }
        };

        const config = statusConfig[result.status];

        return `
            <div class="validation-result ${config.class}">
                <div class="validation-icon-container ${config.class}">
                    <i data-lucide="${config.icon}" style="width: 48px; height: 48px; color: white;"></i>
                </div>
                <h2 class="validation-title ${config.class}">${config.title}</h2>
                <div class="validation-details">
                    <div class="validation-detail-row">
                        <span class="validation-detail-label">Código:</span>
                        <span>${result.ticketCode}</span>
                    </div>
                    ${result.eventName ? `
                        <div class="validation-detail-row">
                            <span class="validation-detail-label">Evento:</span>
                            <span>${result.eventName}</span>
                        </div>
                        <div class="validation-detail-row">
                            <span class="validation-detail-label">Usuario:</span>
                            <span>${result.userName}</span>
                        </div>
                        <div class="validation-detail-row">
                            <span class="validation-detail-label">Asiento:</span>
                            <span>${result.seat}</span>
                        </div>
                    ` : ''}
                </div>
                <p class="validation-message ${config.class}">${config.message}</p>
            </div>
        `;
    }
};
