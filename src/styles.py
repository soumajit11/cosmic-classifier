import streamlit as st
import streamlit.components.v1 as components

# Function to inject particle background and parent document style overrides
def load_parent_enhancements():
    components.html("""
        <script>
            (function() {
                const parentDoc = window.parent.document;
                const parentWin = window.parent;
                
                // Inject CSS style sheet to parent document if not present
                let customStyle = parentDoc.getElementById('custom-streamlit-styles');
                if (!customStyle) {
                    customStyle = parentDoc.createElement('style');
                    customStyle.id = 'custom-streamlit-styles';
                    customStyle.innerHTML = `
                        /* Primary Action Buttons */
                        .btn-primary {
                            background: linear-gradient(135deg, #64ffda 0%, #00b4d8 100%) !important;
                            color: #020610 !important;
                            border: none !important;
                            font-weight: 700 !important;
                            box-shadow: 0 0 20px rgba(100, 255, 218, 0.2) !important;
                            transition: all 0.3s ease !important;
                            border-radius: 25px !important;
                        }
                        .btn-primary:hover {
                            transform: translateY(-2px) !important;
                            box-shadow: 0 0 30px rgba(100, 255, 218, 0.45) !important;
                        }

                        /* Secondary Action Buttons */
                        .btn-secondary {
                            background: linear-gradient(135deg, #102a45 0%, #07162c 100%) !important;
                            border: 1px solid rgba(100, 255, 218, 0.25) !important;
                            color: #64ffda !important;
                            transition: all 0.3s ease !important;
                            border-radius: 25px !important;
                        }
                        .btn-secondary:hover {
                            background: linear-gradient(135deg, #64ffda 0%, #00b4d8 100%) !important;
                            color: #020610 !important;
                            border-color: transparent !important;
                            box-shadow: 0 0 20px rgba(100, 255, 218, 0.3) !important;
                            transform: translateY(-2px) !important;
                        }

                        /* Navbar Buttons - Active */
                        .btn-nav-active {
                            background: rgba(100, 255, 218, 0.08) !important;
                            border: 1px solid #64ffda !important;
                            color: #64ffda !important;
                            border-radius: 20px !important;
                            box-shadow: 0 0 10px rgba(100, 255, 218, 0.1) !important;
                            font-size: 0.85rem !important;
                            font-weight: 600 !important;
                            padding: 6px 18px !important;
                            transition: all 0.3s ease !important;
                        }

                        /* Navbar Buttons - Inactive */
                        .btn-nav-inactive {
                            background: rgba(255, 255, 255, 0.03) !important;
                            border: 1px solid rgba(255, 255, 255, 0.08) !important;
                            color: #8892b0 !important;
                            border-radius: 20px !important;
                            box-shadow: none !important;
                            font-size: 0.85rem !important;
                            font-weight: 500 !important;
                            padding: 6px 18px !important;
                            transition: all 0.3s ease !important;
                        }
                        .btn-nav-inactive:hover {
                            border-color: #64ffda !important;
                            color: #64ffda !important;
                            background: rgba(100, 255, 218, 0.05) !important;
                        }
                    `;
                    parentDoc.head.appendChild(customStyle);
                }

                // Function to classify and apply classes to buttons
                function classifyButtons() {
                    const buttons = parentDoc.querySelectorAll('button');
                    buttons.forEach(btn => {
                        const txt = btn.textContent.trim();
                        
                        // Clean up classes first
                        btn.classList.remove('btn-primary', 'btn-secondary', 'btn-nav-active', 'btn-nav-inactive');
                        
                        if (txt.includes('Welcome') || txt.includes('Configure Parameters') || txt.includes('Diagnostic Report')) {
                            if (txt.startsWith('[') && txt.endsWith(']')) {
                                btn.classList.add('btn-nav-active');
                            } else {
                                btn.classList.add('btn-nav-inactive');
                            }
                        } else if (txt.includes('Run Cosmic') || txt.includes('Access Telemetry') || txt.includes('Export')) {
                            btn.classList.add('btn-primary');
                        } else if (txt.includes('Return to Port') || txt.includes('Adjust Parameters')) {
                            btn.classList.add('btn-secondary');
                        }
                    });
                }

                // Run classifyButtons periodically
                if (!parentWin.buttonStylingInterval) {
                    parentWin.buttonStylingInterval = setInterval(classifyButtons, 100);
                }

                if (parentWin.particleCanvasInitialized) return;
                
                let canvas = parentDoc.getElementById('particle-canvas');
                if (!canvas) {
                    canvas = parentDoc.createElement('canvas');
                    canvas.id = 'particle-canvas';
                    canvas.style.position = 'fixed';
                    canvas.style.top = '0';
                    canvas.style.left = '0';
                    canvas.style.width = '100vw';
                    canvas.style.height = '100vh';
                    canvas.style.zIndex = '-1';
                    canvas.style.pointerEvents = 'none';
                    parentDoc.body.appendChild(canvas);
                }
                
                parentWin.particleCanvasInitialized = true;
                const ctx = canvas.getContext('2d');
                let particles = [];
                let mouse = { x: null, y: null, radius: 150 };

                function resizeCanvas() {
                    canvas.width = parentWin.innerWidth;
                    canvas.height = parentWin.innerHeight;
                    initParticles();
                }

                class Particle {
                    constructor(x, y) {
                        this.x = x;
                        this.y = y;
                        this.size = Math.random() * 2 + 0.8;
                        this.speedX = (Math.random() - 0.5) * 0.35;
                        this.speedY = (Math.random() - 0.5) * 0.35;
                        this.alpha = Math.random() * 0.45 + 0.15;
                    }
                    draw() {
                        ctx.fillStyle = `rgba(100, 255, 218, ${this.alpha})`;
                        ctx.beginPath();
                        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                        ctx.closePath();
                        ctx.fill();
                    }
                    update() {
                        this.x += this.speedX;
                        this.y += this.speedY;

                        if (this.x < 0) this.x = canvas.width;
                        if (this.x > canvas.width) this.x = 0;
                        if (this.y < 0) this.y = canvas.height;
                        if (this.y > canvas.height) this.y = 0;

                        if (mouse.x !== null && mouse.y !== null) {
                            let dx = mouse.x - this.x;
                            let dy = mouse.y - this.y;
                            let distance = Math.sqrt(dx * dx + dy * dy);
                            if (distance < mouse.radius) {
                                let forceDirectionX = dx / distance;
                                let forceDirectionY = dy / distance;
                                let force = (mouse.radius - distance) / mouse.radius;
                                this.x -= forceDirectionX * force * 3.0;
                                this.y -= forceDirectionY * force * 3.0;
                            }
                        }
                    }
                }

                function initParticles() {
                    particles = [];
                    const numberOfParticles = Math.floor((canvas.width * canvas.height) / 20000);
                    for (let i = 0; i < numberOfParticles; i++) {
                        let x = Math.random() * canvas.width;
                        let y = Math.random() * canvas.height;
                        particles.push(new Particle(x, y));
                    }
                }

                function animate() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    for (let i = 0; i < particles.length; i++) {
                        particles[i].update();
                        particles[i].draw();
                    }
                    requestAnimationFrame(animate);
                }

                parentWin.addEventListener('resize', resizeCanvas);
                
                parentWin.addEventListener('mousemove', function(event) {
                    mouse.x = event.clientX;
                    mouse.y = event.clientY;
                });

                parentWin.addEventListener('mouseout', function() {
                    mouse.x = null;
                    mouse.y = null;
                });

                resizeCanvas();
                animate();
            })();
        </script>
    """, height=0, width=0)

# Custom CSS and Styling for the redesigned workspace
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .stApp {
            background: radial-gradient(circle at center, #071120 0%, #010408 100%) !important;
            color: white;
            font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Transparent Streamlit Header */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Spacious Containers */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }

        /* Glassmorphic Panels & Streamlit Border Containers */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(10, 25, 47, 0.45) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(100, 255, 218, 0.08) !important;
            border-radius: 16px !important;
            padding: 25px 30px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }

        .glass-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(100, 255, 218, 0.2) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 40px 0 rgba(100, 255, 218, 0.05) !important;
        }

        /* Slider Containers (for Input Page) */
        .slider-container {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 5px;
            transition: all 0.2s ease;
        }

        .slider-container:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(100, 255, 218, 0.12);
        }

        /* Custom buttons default styling */
        .stButton > button {
            transition: all 0.3s ease;
            cursor: pointer;
            width: 100%;
        }

        /* Headers & Titles */
        .main-title {
            text-align: center !important;
            font-size: 3.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 40%, #64ffda 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
            margin-bottom: 5px;
            display: block !important;
        }

        .main-subtitle {
            text-align: center !important;
            color: #a8b2d1 !important;
            font-size: 1.1rem !important;
            max-width: 800px !important;
            margin: 0 auto 30px auto !important;
            line-height: 1.6 !important;
            display: block !important;
        }

        /* Navigation step indicator */
        .step-indicator {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            margin-top: 5px;
        }

        /* Prediction Card custom dashboard styling */
        .prediction-card-custom {
            padding: 35px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 25px;
            border: 1px solid;
            transition: all 0.3s ease;
        }

        .prediction-class-name {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 12px 0;
            letter-spacing: -0.5px;
        }

        .confidence-container {
            max-width: 420px;
            margin: 20px auto 0 auto;
        }

        .confidence-bg {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            height: 8px;
            width: 100%;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .confidence-bar {
            height: 100%;
            border-radius: 8px;
        }

        /* Class list for landing page */
        .class-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-top: 20px;
        }

        .class-badge {
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #ccd6f6;
        }

        /* Custom tabs override for spaciousness */
        .stTabs [data-baseweb="tab-list"] {
            gap: 18px;
            justify-content: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            color: #8892b0 !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: #64ffda !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #64ffda !important;
            border-bottom: 2px solid #64ffda !important;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #64ffda !important;
        }
        </style>
    """, unsafe_allow_html=True)
