import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request, cookies }) => {
    const API_URL = import.meta.env.PUBLIC_WEBHOOK_URL || 'http://recruiter-dev-n8n:5678/webhook/ask';
    
    // Get or create session ID
    let sessionId = cookies.get('sessionId');
    if (!sessionId) {
        sessionId = crypto.randomUUID();
        cookies.set('sessionId', sessionId, { path: '/' });
    }

    try {
        const { chatInput } = await request.json();
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chatInput,
                sessionId
            })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch from webhook');
        }

        const data = await response.json();
        return json({ output: data.output });
    } catch (error) {
        console.error('Error in chat endpoint:', error);
        return json({ error: 'Failed to process message' }, { status: 500 });
    }
};