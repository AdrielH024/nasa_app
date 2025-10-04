document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault(); 
        console.log(`Navegando para: ${event.target.textContent}`);
        
        document.querySelectorAll('nav a').forEach(l => {
            l.classList.remove('bg-red-600', 'rounded-t-lg', 'font-semibold');
            l.classList.add('hover:bg-white/20', 'rounded-md'); // Adiciona de volta o estilo hover padrão
        });
        
        event.target.classList.add('bg-red-600', 'rounded-t-lg', 'font-semibold');
        event.target.classList.remove('hover:bg-white/20', 'rounded-md');
    });
});