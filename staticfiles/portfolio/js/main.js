document.addEventListener("DOMContentLoaded", () => {

    /* ========================================
       PREMIUM PORTFOLIO INTERACTIONS
    ======================================== */

    const navbar = document.querySelector(".navbar");

    const revealElements = document.querySelectorAll(
        `
        .section-heading,
        .project-card,
        .about-content,
        .about-stats,
        .skill-category,
        .service-card,
        .contact-card,
        .contact-content,
        .footer-cta,
        .footer-main
        `
    );


    /* ========================================
       NAVBAR ON SCROLL
    ======================================== */

    const updateNavbar = () => {

        if (!navbar) return;

        if (window.scrollY > 30) {
            navbar.classList.add("navbar-scrolled");
        } else {
            navbar.classList.remove("navbar-scrolled");
        }

    };

    updateNavbar();

    window.addEventListener(
        "scroll",
        updateNavbar,
        { passive: true }
    );


    /* ========================================
       REVEAL ON SCROLL
    ======================================== */

    const prefersReducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (prefersReducedMotion) {

        revealElements.forEach((element) => {
            element.classList.add("reveal-visible");
        });

    } else {

        revealElements.forEach((element, index) => {

            element.classList.add("reveal");

            /*
             Small stagger effect.
             Limited so animations never become too slow.
            */

            const delay =
                Math.min((index % 3) * 80, 160);

            element.style.setProperty(
                "--reveal-delay",
                `${delay}ms`
            );

        });


        const revealObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach((entry) => {

                        if (!entry.isIntersecting) return;

                        entry.target.classList.add(
                            "reveal-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.12,
                    rootMargin:
                        "0px 0px -50px 0px",
                }
            );


        revealElements.forEach((element) => {
            revealObserver.observe(element);
        });

    }


    /* ========================================
       SMOOTH INTERNAL LINKS
    ======================================== */

    const internalLinks =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    internalLinks.forEach((link) => {

        link.addEventListener(
            "click",
            (event) => {

                const targetId =
                    link.getAttribute("href");

                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    return;
                }

                const target =
                    document.querySelector(
                        targetId
                    );

                if (!target) return;

                event.preventDefault();

                target.scrollIntoView({
                    behavior:
                        prefersReducedMotion
                            ? "auto"
                            : "smooth",
                    block: "start",
                });

            }
        );

    });


    /* ========================================
       CLOSE MOBILE NAV AFTER CLICK
    ======================================== */

    const navbarCollapse =
        document.querySelector(
            ".navbar-collapse"
        );

    const navLinks =
        document.querySelectorAll(
            ".navbar-nav .nav-link"
        );


    navLinks.forEach((link) => {

        link.addEventListener(
            "click",
            () => {

                if (!navbarCollapse) return;

                if (
                    navbarCollapse.classList.contains(
                        "show"
                    )
                ) {

                    const bootstrapCollapse =
                        bootstrap.Collapse.getOrCreateInstance(
                            navbarCollapse
                        );

                    bootstrapCollapse.hide();

                }

            }
        );

    });

/* ========================================
   ACTIVE NAV LINK ON SCROLL
======================================== */

const sections = document.querySelectorAll(
    "section[id]"
);

const sectionNavLinks =
    document.querySelectorAll(
        '.navbar .nav-link[href^="#"]'
    );


const updateActiveNav = () => {

    let currentSectionId = "";

    const scrollPosition =
        window.scrollY + 140;


    sections.forEach((section) => {

        const sectionTop =
            section.offsetTop;

        const sectionHeight =
            section.offsetHeight;

        if (
            scrollPosition >= sectionTop &&
            scrollPosition <
            sectionTop + sectionHeight
        ) {
            currentSectionId =
                section.getAttribute("id");
        }

    });


    sectionNavLinks.forEach((link) => {

        link.classList.remove("active");

        const href =
            link.getAttribute("href");

        if (
            href === `#${currentSectionId}`
        ) {
            link.classList.add("active");
        }

    });

};


updateActiveNav();

window.addEventListener(
    "scroll",
    updateActiveNav,
    { passive: true }
);});