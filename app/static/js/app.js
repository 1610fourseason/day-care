document.addEventListener('DOMContentLoaded', () => {
    pageAdminBlog();
    pageBlogCreate();
    initScrollReveal(); 
});

 // 削除モーダルの処理
function pageAdminBlog(){
    const modal = document.querySelector('#deleteModal');
    if (!modal) return;

    const titleEl = document.querySelector('#deleteTitle');
    const form = document.querySelector('#deleteForm');


    modal.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        console.log('押されたボタン:', button);
        console.log('data-delete-url:', button.dataset.deleteUrl);
        const title = button.dataset.title;
        titleEl.textContent = title
        form.action = button.dataset.deleteUrl;

        console.log('form.action セット後:', form.action);
    });
}


function pageBlogCreate(){
    const blogCreateForm = document.querySelector('#blogCreateForm');
    if (!blogCreateForm) return;

    const submitBtn = document.querySelector('#submitBtn');
    const loadingBtn = document.querySelector('#loadingBtn');

    blogCreateForm.addEventListener('submit', () =>{
        submitBtn.classList.add('d-none');

        loadingBtn.classList.remove('d-none');
    });

}

function initScrollReveal(){
    const targets = document.querySelectorAll('.reveal');
    if (!targets.length) return;

    const observer = new IntersectionObserver((entries, obs)=>{
        for (const entry of entries){
            if (!entry.isIntersecting) continue;

            entry.target.classList.add('is-visible');

            obs.unobserve(entry.target);
        }
    },{
        root:null,
        rootMargin: '0px 0px -10% 0px', 
        threshold: 0.15
    });

    for (const element of targets){
        observer.observe(element);
    }
}
