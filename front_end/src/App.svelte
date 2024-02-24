<script>
  import SignUp from './lib/SignUp.svelte';
  import Login from './lib/Login.svelte';
  import AllRecipes from './lib/AllRecipes.svelte';
  
  let showSignUp = false;
  let authToken = null;
</script>

<main>
{#if showSignUp}
<SignUp></SignUp>
<div id="log-in-msg">
Already have an account? 
<button type="submit" on:click={() => showSignUp = false}>Log in</button>
</div>
{:else}
<Login></Login>
<div id="create-account-msg">
Don't have an account? 
<button type="submit" on:click={() => showSignUp = true}>Create Account</button>
</div>
{/if}

{#if authToken != null}
<h2>Post recipe</h2>
{/if}

<h2>Check out all out content:</h2>
<AllRecipes></AllRecipes>
</main>
