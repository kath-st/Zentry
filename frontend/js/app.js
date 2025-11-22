// Archivo principal de la aplicación

// Variables globales para la selección de asientos
let selectedSeats = new Set();

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    // Renderizar la aplicación inicial
    AppState.render();
    
    // Configurar event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Event listener para el formulario de login
    document.addEventListener('submit', (e) => {
        if (e.target.id === 'login-form') {
            e.preventDefault();
            handleLogin(e);
        }
    });
}

// Manejar login
function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorContainer = document.getElementById('error-container');
    
    // Credenciales del sistema
    const credentials = {
        client: { email: 'cliente@zentry.com', password: 'Zentry123' },
        staff: { email: 'staff@zentry.com', password: 'Access2025' }
    };
    
    // Simular delay de autenticación
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Verificando...';
    
    setTimeout(() => {
        if (credentials.client.email === email && credentials.client.password === password) {
            AppState.login('client');
        } else if (credentials.staff.email === email && credentials.staff.password === password) {
            AppState.login('staff');
        } else {
            errorContainer.innerHTML = `
                <div class="error-message">
                    Credenciales incorrectas. Por favor, verifica tus datos.
                </div>
            `;
            submitBtn.disabled = false;
            submitBtn.textContent = 'Iniciar sesión';
        }
    }, 800);
}

// Actualizar filtros de eventos
function updateEventFilters() {
    const filterCategory = document.getElementById('filter-category').value;
    const sortBy = document.getElementById('sort-by').value;
    
    const eventsGrid = document.getElementById('events-grid');
    eventsGrid.innerHTML = Components.renderEventCards(filterCategory, sortBy);
    initLucideIcons();
}

// Manejar selección de asientos
function toggleSeat(seatId, zone, price, row, number) {
    const seatButton = document.querySelector(`button[data-seat-id="${seatId}"]`);
    
    if (selectedSeats.has(seatId)) {
        selectedSeats.delete(seatId);
        seatButton.classList.remove('selected');
    } else {
        selectedSeats.add(seatId);
        seatButton.classList.add('selected');
    }
    
    updateSeatSummary();
}

function updateSeatSummary() {
    const summaryCount = document.getElementById('summary-seats-count');
    const summaryActions = document.getElementById('summary-actions');
    const floatingSummary = document.getElementById('floating-summary');
    
    const cartItemsCount = AppState.cartItems.length;
    const cartTotal = AppState.cartItems.reduce((sum, item) => sum + item.price, 0);
    
    if (summaryCount) {
        summaryCount.textContent = `${cartItemsCount} asientos reservados`;
    }
    
    if (selectedSeats.size > 0) {
        const total = calculateSelectedSeatsTotal();
        

        
        // Mostrar resumen flotante
        floatingSummary.innerHTML = `
            <div class="cart-summary-floating">
                <div class="cart-summary-info">
                    <i data-lucide="users" style="width: 24px; height: 24px; color: white;"></i>
                    <div>
                        <p class="cart-summary-text">Asientos seleccionados</p>
                        <p class="cart-summary-count">${selectedSeats.size} entrada(s)</p>
                    </div>
                </div>
                <div class="cart-summary-actions">
                    <div style="text-align: right;">
                        <p class="cart-summary-total-label">Total</p>
                        <p class="cart-summary-total">${formatPrice(total)}</p>
                    </div>
                    <button class="btn btn-white" onclick="addSelectedSeatsToCart()">
                        <i data-lucide="shopping-cart" style="width: 20px; height: 20px;"></i>
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        `;
        initLucideIcons();
    } else {
        // Si no hay asientos seleccionados, el resumen flotante se oculta.
        floatingSummary.innerHTML = '';
    }

    // Lógica para el resumen de la barra lateral (summaryActions)
    // El usuario quiere que el total y el botón 'Ir al carrito' permanezcan visibles
    // en la barra lateral mientras haya al menos un asiento en el carrito (AppState.cartItems.length > 0)
    if (summaryActions) {
        const total = AppState.cartItems.reduce((sum, item) => sum + item.price, 0);
        
        if (AppState.cartItems.length > 0) {
            summaryActions.innerHTML = `
                <div style="border-top: 1px solid rgba(107, 114, 128, 0.5); padding-top: 0.75rem; margin-top: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 0.875rem; color: var(--color-text-muted);">Total</span>
                        <span style="font-size: 1.5rem; font-weight: 700;">
                            ${formatPrice(total)}
                        </span>
                    </div>
                    <button class="btn btn-primary w-full" onclick="AppState.navigate('carrito')">
                        <i data-lucide="shopping-cart" style="width: 16px; height: 16px;"></i>
                        Ir al Carrito
                    </button>
                </div>
            `;
            initLucideIcons();
        } else {
            summaryActions.innerHTML = '';
        }
    }
}

function calculateSelectedSeatsTotal() {
    let total = 0;
    selectedSeats.forEach(seatId => {
        const seatButton = document.querySelector(`button[data-seat-id="${seatId}"]`);
        if (seatButton) {
            const price = parseFloat(seatButton.dataset.seatPrice);
            total += price;
        }
    });
    return total;
}

function addSelectedSeatsToCart() {
    if (selectedSeats.size === 0) {
        toast.error('Selecciona al menos un asiento');
        return;
    }
    
    const eventId = AppState.selectedEventId;
    const seatsToAdd = [];
    
    // Recolectar todos los asientos primero
    selectedSeats.forEach(seatId => {
        const seatButton = document.querySelector(`button[data-seat-id="${seatId}"]`);
        if (seatButton) {
            const zone = seatButton.dataset.seatZone;
            const price = parseFloat(seatButton.dataset.seatPrice);
            const [, rowPart, numPart] = seatId.split('-');
            const row = parseInt(rowPart.substring(1));
            const number = parseInt(numPart.substring(1));
            
            seatsToAdd.push({
                id: seatId,
                row: row,
                number: number,
                zone: zone,
                price: price,
                available: true
            });
        }
    });
    
    // Agregar todos los asientos al carrito
    seatsToAdd.forEach(seat => {
        AppState.addToCart(seat, eventId);
    });
    
    toast.success(`${seatsToAdd.length} entrada(s) agregada(s) al carrito`);
    
    // Limpiar selección visual
    selectedSeats.forEach(seatId => {
        const seatButton = document.querySelector(`button[data-seat-id="${seatId}"]`);
        if (seatButton) {
            seatButton.classList.remove('selected');
        }
    });
    selectedSeats.clear();
    
    // Actualizar UI
    updateSeatSummary();
    AppState.render();
}

// Validación de tickets (Staff)
function handleValidation(e) {
    e.preventDefault();
    
    const ticketCode = document.getElementById('ticket-code').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const resultContainer = document.getElementById('validation-result');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Validando...';
    
    // Simular llamada a API
    setTimeout(() => {
        let status;
        let result;
        
        if (ticketCode.startsWith('VALID')) {
            status = 'valid';
            result = {
                status,
                ticketCode,
                eventName: 'Festival Electrónico 2025',
                userName: 'Juan Pérez',
                seat: 'VIP-A12'
            };
        } else if (ticketCode.startsWith('USED')) {
            status = 'used';
            result = {
                status,
                ticketCode,
                eventName: 'Noche de Rock Clásico',
                userName: 'María González',
                seat: 'PREF-B08'
            };
        } else {
            status = 'invalid';
            result = {
                status,
                ticketCode
            };
        }
        
        resultContainer.innerHTML = Components.renderValidationResult(result);
        initLucideIcons();
        
        submitBtn.disabled = false;
        submitBtn.textContent = 'Validar Ticket';
    }, 1000);
}

function resetValidation() {
    document.getElementById('ticket-code').value = '';
    document.getElementById('validation-result').innerHTML = '';
}

// Exponer funciones globalmente para que puedan ser llamadas desde onclick
window.toggleSeat = toggleSeat;
window.addSelectedSeatsToCart = addSelectedSeatsToCart;
window.validateTicket = validateTicket;
window.resetValidation = resetValidation;
