import "./header.css"

function Header() {

    return (
        <header className="app-header">

            <div className="header-content">

                <a href="/" className="logo">
                    <img src="src/assets/image.png"></img>
                    IBE CHECK
                </a>

                <nav className="header-nav">

                    <a href="#about">
                        About
                    </a>

                    <a
                        href="https://github.com/ayaan0604/vibe-check"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        GitHub
                    </a>

                </nav>

            </div>

        </header>
    )
}

export default Header