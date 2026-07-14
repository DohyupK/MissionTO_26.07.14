export default function MyHeader({ email, isLogin = false }) {
    // var ui;
    // if (isLogin = true) {
    //     ui = (<button type="button" className="header__btn header__btn--logout">로그아웃</button>)
    // } else {
    //     ui = (
    //         <>
    //             <button type="button" className="header__btn header__btn--login">로그인</button>
    //             <button type="button" className="header__btn header__btn--signup">회원가입</button>
    //         </>
    //     )
    // }

    return (
        <header className="header">
            <div className="header__user">
                <span className="header__avatar" aria-hidden="true">JM</span>
                <div className="header__info">
                    <span className="header__label">로그인 계정</span>
                    <span className="header__email">{email}</span>
                </div>
            </div>
            <div className="header__buttons">
                {isLogin == true ?
                    <button type="button" className="header__btn header__btn--logout">로그아웃</button>
                    :
                    <>
                        <button type="button" className="header__btn header__btn--login">로그인</button>
                        <button type="button" className="header__btn header__btn--signup">회원가입</button>
                    </>
                }
            </div>
        </header>
    )
}