// Gestión de estado de la aplicación

const AppState = {
    // Estado actual
    userType: null, // 'client' | 'staff' | null
    currentPage: 'login', // 'login' | 'home' | 'eventos' | 'detalle' | 'carrito' | 'mis-compras' | 'validation'
    selectedEventId: null,
    cartItems: [],
    cartHistory: [],
    purchases: [],
    reservedSeats: new Set(),
    timeRemaining: 300, // 5 minutos en segundos
    timerActive: false,
    timerInterval: null,
    generatedSeats: {}, // Almacenar asientos generados por evento

    // Datos de eventos
    eventData: {
        1: { name: "Festival Electrónico 2025", date: "15 de Noviembre, 2025", venue: "Estadio Nacional", time: "20:00 hrs" },
        2: { name: "Noche de Rock Clásico", date: "22 de Noviembre, 2025", venue: "Arena Central", time: "21:00 hrs" },
        3: { name: "Jazz en la Ciudad", date: "28 de Noviembre, 2025", venue: "Teatro Municipal", time: "19:30 hrs" },
        4: { name: "Pop Latino Tour", date: "5 de Diciembre, 2025", venue: "Auditorio Nacional", time: "20:30 hrs" },
        5: { name: "Techno Underground", date: "10 de Diciembre, 2025", venue: "Club Nocturno", time: "23:00 hrs" },
        6: { name: "Indie Fest 2025", date: "18 de Diciembre, 2025", venue: "Parque de la Música", time: "18:00 hrs" }
    },

    events: [
        {
            id: 1,
            name: "Festival Electrónico 2025",
            date: "15 de Noviembre, 2025",
            venue: "Estadio Nacional",
            image: "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?w=1080&q=80",
            price: 45,
            available: 500,
            category: "electronica",
            popular: true
        },
        {
            id: 2,
            name: "Noche de Rock Clásico",
            date: "22 de Noviembre, 2025",
            venue: "Arena Central",
            image: "https://images.unsplash.com/photo-1574154945982-0c7aff5adaef?w=1080&q=80",
            price: 38,
            available: 320,
            category: "rock",
            popular: true
        },
        {
            id: 3,
            name: "Jazz en la Ciudad",
            date: "28 de Noviembre, 2025",
            venue: "Teatro Municipal",
            image: "https://images.unsplash.com/photo-1709731191876-899e32264420?w=1080&q=80",
            price: 52,
            available: 180,
            category: "jazz"
        },
        {
            id: 4,
            name: "Pop Latino Tour",
            date: "5 de Diciembre, 2025",
            venue: "Auditorio Nacional",
            image: "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?w=1080&q=80",
            price: 60,
            available: 420,
            category: "pop"
        },
        {
            id: 5,
            name: "Techno Underground",
            date: "10 de Diciembre, 2025",
            venue: "Club Nocturno",
            image: "https://images.unsplash.com/photo-1574154945982-0c7aff5adaef?w=1080&q=80",
            price: 35,
            available: 250,
            category: "electronica"
        },
        {
            id: 6,
            name: "Indie Fest 2025",
            date: "18 de Diciembre, 2025",
            venue: "Parque de la Música",
            image: "https://images.unsplash.com/photo-1709731191876-899e32264420?w=1080&q=80",
            price: 42,
            available: 380,
            category: "indie"
        }
    ],

    // Métodos para manejar el estado
    login(type) {
        this.userType = type;
        this.currentPage = type === 'client' ? 'home' : 'validation';
        this.render();
    },

    logout() {
        this.userType = null;
        this.currentPage = 'login';
        this.cartItems = [];
        this.cartHistory = [];
        this.stopTimer();
        this.render();
    },

    navigate(page, eventId = null) {
        if (page === 'detalle' && eventId) {
            this.selectedEventId = eventId;
            this.currentPage = 'detalle';
        } else {
            this.currentPage = page;
        }
        this.render();
    },

    addToCart(seat, eventId) {
        const event = this.eventData[eventId];
        if (!event) return;

        // Guardar estado actual del carrito en el historial
        this.cartHistory.push([...this.cartItems]);

        // Resetear temporizador a 5 minutos
        this.startTimer();

        // Agregar asiento a los reservados
        this.reservedSeats.add(seat.id);

        const newItem = {
            id: generateId(),
            eventId,
            eventName: event.name,
            eventDate: event.date,
            eventVenue: event.venue,
            seatId: seat.id,
            zone: seat.zone,
            price: seat.price
        };

        this.cartItems.push(newItem);
    },

    removeItem(itemId) {
        // Guardar estado actual en el historial
        this.cartHistory.push([...this.cartItems]);

        // Remover el asiento de los reservados
        const itemToRemove = this.cartItems.find(item => item.id === itemId);
        if (itemToRemove) {
            this.reservedSeats.delete(itemToRemove.seatId);
        }

        this.cartItems = this.cartItems.filter(item => item.id !== itemId);

        // Si el carrito queda vacío, detener el temporizador
        if (this.cartItems.length === 0) {
            this.stopTimer();
        } else {
            // Si aún hay items, resetear el temporizador
            this.timeRemaining = 300;
        }

        toast.success("Entrada eliminada del carrito");
        this.render();
    },

    undo() {
        if (this.cartHistory.length === 0) return;

        // Restaurar el último estado del carrito
        const previousState = this.cartHistory.pop();

        // Reconstruir los asientos reservados
        this.reservedSeats = new Set();
        previousState.forEach(item => {
            this.reservedSeats.add(item.seatId);
        });

        this.cartItems = previousState;

        // Si el carrito queda vacío después de deshacer, detener el temporizador
        if (this.cartItems.length === 0) {
            this.stopTimer();
        } else {
            this.timeRemaining = 300;
        }

        toast.success("Acción deshecha");
        this.render();
    },

    checkout() {
        if (this.cartItems.length === 0) return;

        // Detener el temporizador
        this.stopTimer();
        this.reservedSeats = new Set();

        // Agrupar items por evento
        const groupedByEvent = {};
        this.cartItems.forEach(item => {
            if (!groupedByEvent[item.eventId]) {
                groupedByEvent[item.eventId] = [];
            }
            groupedByEvent[item.eventId].push(item);
        });

        // Crear purchases por cada evento
        const newPurchases = Object.entries(groupedByEvent).map(([eventId, items]) => {
            const subtotal = items.reduce((sum, item) => sum + item.price, 0);
            const total = subtotal * 1.1; // Incluir cargo por servicio
            
            return {
                id: `PURCHASE-${Date.now()}-${eventId}`,
                eventName: items[0].eventName,
                eventDate: items[0].eventDate,
                eventVenue: items[0].eventVenue,
                purchaseDate: formatDate(new Date()),
                seats: items.map(item => ({
                    seatId: item.seatId,
                    zone: item.zone,
                    price: item.price
                })),
                total,
                qrCode: `VALID-${Math.random().toString(36).substring(2, 10).toUpperCase()}`
            };
        });

        this.purchases = [...newPurchases, ...this.purchases];
        this.cartItems = [];
        this.cartHistory = [];
        
        toast.success("¡Compra realizada con éxito! Tus tickets han sido enviados.");
        this.navigate('mis-compras');
    },

    startTimer() {
        this.timerActive = true;
        this.timeRemaining = 300;

        // Limpiar intervalo anterior si existe
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }

        this.timerInterval = setInterval(() => {
            this.timeRemaining--;

            if (this.timeRemaining <= 0) {
                // Tiempo expirado
                this.stopTimer();
                this.reservedSeats = new Set();
                this.cartItems = [];
                this.cartHistory = [];
                toast.error("Expiración del Tiempo de Compra: No pudimos guardar tu reserva por más tiempo. Para continuar con tu compra por favor empieza de nuevo.");
                this.render();
            } else {
                // Actualizar solo el temporizador sin re-renderizar toda la página
                this.updateTimer();
            }
        }, 1000);
    },

    stopTimer() {
        this.timerActive = false;
        this.timeRemaining = 300;
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    },

    updateTimer() {
        const timerElement = document.querySelector('.timer-value');
        if (timerElement) {
            timerElement.textContent = formatTime(this.timeRemaining);
            
            // Cambiar estilo si queda menos de 1 minuto
            const timerBox = document.querySelector('.timer-box');
            if (timerBox) {
                if (this.timeRemaining <= 60) {
                    timerBox.className = 'timer-box warning';
                    timerElement.className = 'timer-value warning';
                } else {
                    timerBox.className = 'timer-box normal';
                    timerElement.className = 'timer-value normal';
                }
            }
        }
    },

    render() {
        const app = document.getElementById('app');
        app.innerHTML = Components.renderApp(this);
        initLucideIcons();
        
        // Si estamos en la página de detalle, actualizar el resumen
        if (this.currentPage === 'detalle' && typeof updateSeatSummary === 'function') {
            updateSeatSummary();
        }
    }
};
