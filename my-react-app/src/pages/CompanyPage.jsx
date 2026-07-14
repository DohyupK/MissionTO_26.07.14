import MyHeader from "../components/MyHeader"

export default function CompanyPage() {
    return (
        <>
            <MyHeader email="test@example.com" isLogin={false} />
            <h1>Company Page</h1>
        </>
    )
}