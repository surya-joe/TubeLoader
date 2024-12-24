import { NextResponse } from "next/server";

export async function POST(req: Request) {
    try{
        const { url, preference, output_path } = await req.json();
        console.log('route : ', url, preference, output_path)
        
        const response = await fetch(
            "http://127.0.0.1:5000/download", 
            {
                method: "POST",
                headers: { 'content-type': 'application/json' }, 
                body: JSON.stringify({ url, preference, output_path})
            }
        );

        const data = await response.json();

        if (response.ok) {
            return NextResponse.json({message : data.message})
        } else {
            return NextResponse.json({error : data.error}, {status:response.status})
        }

    }
    catch (error) {
        return NextResponse.json({error : "An exception occurred"}, {status: 500})
    }
}