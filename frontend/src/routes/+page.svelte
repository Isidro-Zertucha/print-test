<script lang="ts">    
    let inputText: string = '';
    let messages: { text: string; sender: 'user' | 'bot'; error?: boolean }[] = [];
    
    async function sendMessage() {
        if (!inputText.trim()) return;

        const userMessage = {
            text: inputText,
            sender: 'user' as const
        };
        messages = [...messages, userMessage];
        inputText = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    chatInput: userMessage.text
                })
            });

            if (response.ok) {
                const data = await response.json();
                messages = [
                    ...messages,
                    { text: data.output, sender: 'bot' }
                ];
            } else {
                throw new Error('Server error');
            }
        } catch (error) {
            console.error('Error:', error);
            messages = [
                ...messages,
                { text: 'Error communicating with the bot.', sender: 'bot', error: true }
            ];
        }
    }
</script>

<div class="chat-wrapper">
	<div class="chatbot-container">
		<div class="message-area">
			{#each messages as message}
				<div class={`message ${message.sender}`}>
					{message.text}
					{#if message.error}
						<span class="error-indicator">(Error)</span>
					{/if}
				</div>
			{/each}
		</div>
		<div class="input-area">
			<input
				type="text"
				bind:value={inputText}
				placeholder="Type your message..."
				on:keydown={(event) => event.key === 'Enter' && sendMessage()}
			/>
			<button on:click={sendMessage}>Send</button>
		</div>
	</div>
</div>

<style>
	.chat-wrapper {
		display: flex;
		justify-content: center;
		padding: 1rem;
		width: 100%;
		max-width: 1200px;
		margin: 0 auto;
	}

	.chatbot-container {
		display: flex;
		flex-direction: column;
		height: 70vh;
		width: 100%;
		max-width: 800px;
		border: 1px solid #ccc;
		border-radius: 8px;
		overflow: hidden;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		background: white;
	}

	.message-area {
		flex-grow: 1;
		padding: 20px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.message {
		padding: 12px 16px;
		border-radius: 12px;
		max-width: 80%;
		word-wrap: break-word;
		line-height: 1.4;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.user {
		background-color: #e0f7fa;
		align-self: flex-end;
		border-bottom-right-radius: 4px;
	}

	.bot {
		background-color: #f0f0f0;
		align-self: flex-start;
		border-bottom-left-radius: 4px;
	}

	.error-indicator {
		font-size: 0.8em;
		color: red;
		margin-left: 5px;
	}

	.input-area {
    display: flex;
    padding: 12px;
    border-top: 1px solid #ccc;
    background: #f9f9f9;
    gap: 8px;
  }

  .input-area input {
    flex-grow: 1;
    min-width: 0; /* Allows input to shrink properly */
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 20px;
    outline: none;
    font-size: 0.9rem;
  }

  .input-area button {
    padding: 10px 16px;
    min-width: fit-content; /* Prevents button from shrinking too much */
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.2s;
    white-space: nowrap; /* Prevents text wrapping */
  }

  /* Special handling for very small screens */
  @media (max-width: 400px) {
    .input-area {
      padding: 8px;
      flex-wrap: wrap; /* Allows button to move below on tiny screens */
    }
    
    .input-area input {
      min-width: 100%; /* Full width on smallest screens */
      order: 1; /* Moves input to top */
      border-radius: 20px 20px 0 0;
    }
    
    .input-area button {
      min-width: 100%; /* Full width button */
      order: 2; /* Moves button below */
      border-radius: 0 0 20px 20px;
      padding: 12px; /* More touch-friendly */
    }
  }

  @media (max-width: 300px) {
    .message {
      max-width: 95%; /* More space for messages on tiny screens */
      padding: 10px 12px;
      font-size: 0.9rem;
    }
  }
</style>
