import MyHeader from "../components/MyHeader"

export default function HomePage() {
    return (
        <>
            <MyHeader email="jm@example.com" isLogin={true} />
            <h1>Home Page</h1>
        </>
    )
}