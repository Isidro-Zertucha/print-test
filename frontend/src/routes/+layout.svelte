<script lang="ts">
	import '../app.css';
	
	let { children } = $props();
</script>
<div>
	<h1>PrintAI ChatBot</h1>
</div>

{@render children()}

<style>
	div {
	  display: flex;
	  justify-content: center;
	  padding: 1rem;
	  width: 100%;
	}
  
	h1 {
	  text-align: center;
	}
  </style>

  