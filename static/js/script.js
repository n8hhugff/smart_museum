/* =====================================================
   SMART MUSEUM – INTERACTIVE SCRIPT
   ===================================================== */

// عند تحميل الصفحة
document.addEventListener("DOMContentLoaded", () => {
  console.log(" المتحف الذكي جاهز للعمل!");

  /* =============================
     فلترة الأعمال الفنية حسب الفئة
     ============================= */
  const filterButtons = document.querySelectorAll(".filter-btn");
  const exhibits = document.querySelectorAll(".exhibit-card");

  filterButtons.forEach(button => {
    button.addEventListener("click", () => {
      // إزالة الحالة النشطة عن جميع الأزرار
      filterButtons.forEach(btn => btn.classList.remove("active"));
      button.classList.add("active");

      const category = button.dataset.category;
      exhibits.forEach(exhibit => {
        if (category === "all" || exhibit.dataset.category === category) {
          exhibit.style.display = "block";
          exhibit.classList.add("fade-in");
        } else {
          exhibit.style.display = "none";
          exhibit.classList.remove("fade-in");
        }
      });
    });
  });

  /* =============================
     تأثيرات دخول بطاقات المعرض
     ============================= */
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.2 }
  );

  document.querySelectorAll(".exhibit-card").forEach(card => {
    observer.observe(card);
  });

  /* =============================
     صندوق عرض الصورة (Lightbox)
     ============================= */
  const lightbox = document.createElement("div");
  lightbox.classList.add("lightbox");
  const img = document.createElement("img");
  lightbox.appendChild(img);
  document.body.appendChild(lightbox);

  document.querySelectorAll(".art-image, .exhibit-card img").forEach(image => {
    image.addEventListener("click", e => {
      img.src = e.target.src;
      lightbox.style.display = "flex";
    });
  });

  lightbox.addEventListener("click", () => {
    lightbox.style.display = "none";
  });

  /* =============================
     تأثيرات أزرار التحريك الصغيرة
     ============================= */
  const buttons = document.querySelectorAll("button, .art-actions a");
  buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
      btn.style.transform = "scale(1.05)";
      btn.style.boxShadow = "0 5px 10px rgba(0,0,0,0.2)";
    });
    btn.addEventListener("mouseleave", () => {
      btn.style.transform = "scale(1)";
      btn.style.boxShadow = "none";
    });
  });

  /* =============================
     تأثير الكتابة في قسم البطل (Hero)
     ============================= */
  const heroText = document.querySelector(".hero-content .lead");
  if (heroText) {
    const text = heroText.textContent;
    heroText.textContent = "";
    let i = 0
    const typing = setInterval(() => {
      heroText.textContent += text[i];
      i++;
      if (i >= text.length) clearInterval(typing);
    }, 60);
  }

  /* =============================
     تأثيرات تمرير الصفحة (Scroll)
     ============================= */
  window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 80) {
      navbar.style.background = "#3b2f24";
      navbar.style.boxShadow = "0 3px 12px rgba(0,0,0,0.3)";
    } else {
      navbar.style.background = "#4b3f2f";
      navbar.style.boxShadow = "0 3px 8px rgba(0,0,0,0.15)";
    }
  });

  /* =============================
     لمسة جمالية على صندوق الإجابة
     ============================= */
  const chatbot = document.querySelector(".chatbot-answer");
  if (chatbot) {
    chatbot.style.animation = "fadeInUp 1.2s ease";
  }

  /* =============================
     تحية ذكية للمستخدم
     ============================= */
  setTimeout(() => {
    const hour = new Date().getHours();
    let greeting = "مرحبًا بك في المتحف الذكي!";
    if (hour < 12) greeting = "صباح الإبداع والفن!";
    else if (hour < 18) greeting = "نهارك مليء بالجمال والثقافة!";
    else greeting = "مساء الفن والتاريخ الجميل!";

    console.log(` ${greeting}`);
  }, 500);
});
botSpans.forEach(span => {
  const text = span.innerText.trim();
  span.innerText = "";
  let i = 0;
  function type() {
    if (i < text.length) {
      span.innerHTML += text.charAt(i);
      clickSound.currentTime = 0;
      clickSound.play();
      i++;
      setTimeout(type, 35); // سرعة كتابة مناسبة
    } else {
      // بعد انتهاء الكتابة، يقرأ الروبوت الإجابة كاملة
      speakArabic(text);
    }
  }
  type();
});
