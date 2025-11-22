// Utilidades generales

// Sistema de notificaciones toast
const toast = {
    success: (message) => showToast(message, 'success'),
    error: (message) => showToast(message, 'error'),
    info: (message) => showToast(message, 'info')
};

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toastEl = document.createElement('div');
    toastEl.className = `toast ${type}`;
    
    const iconMap = {
        success: 'check-circle',
        error: 'x-circle',
        info: 'info'
    };
    
    toastEl.innerHTML = `
        <div class="toast-icon">
            <i data-lucide="${iconMap[type]}" style="width: 20px; height: 20px;"></i>
        </div>
        <div class="toast-message">${message}</div>
    `;
    
    container.appendChild(toastEl);
    
    // Inicializar iconos de Lucide
    if (window.lucide) {
        lucide.createIcons();
    }
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toastEl.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            container.removeChild(toastEl);
        }, 300);
    }, 3000);
}

// Formatear tiempo en formato MM:SS
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Formatear precio
function formatPrice(price) {
    return `$${price.toFixed(2)}`;
}

// Formatear fecha
function formatDate(date) {
    return new Date(date).toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    });
}

// Crear elemento con clases y contenido
function createElement(tag, classes = '', content = '') {
    const el = document.createElement(tag);
    if (classes) el.className = classes;
    if (content) el.innerHTML = content;
    return el;
}

// Generar ID único
function generateId() {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

// Animar entrada de elementos
function animateIn(element, delay = 0) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        element.style.transition = 'all 0.5s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, delay);
}

// Inicializar iconos de Lucide después de renderizar
function initLucideIcons() {
    if (window.lucide) {
        lucide.createIcons();
    }
}

// Debounce para optimizar eventos
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
