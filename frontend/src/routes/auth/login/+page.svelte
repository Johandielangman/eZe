<script lang="ts">
	let email = "";
	let password = "";

	const handleLogin = () => {
		// Replace with actual login logic
		console.log("Logging in with", email, password);
	};
</script>

<div class="w-full max-w-sm bg-white rounded-2xl shadow-md p-6">
	<h1 class="text-2xl font-bold mb-6 text-center">Login</h1>

	<form on:submit|preventDefault={handleLogin} class="space-y-4">
		<div>
			<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
			<input
				id="email"
				type="email"
				bind:value={email}
				required
				class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
		</div>

		<div>
			<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
			<input
				id="password"
				type="password"
				bind:value={password}
				required
				class="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
		</div>

		<button
			type="submit"
			class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
		>
			Log In
		</button>
	</form>

	<p class="text-sm text-center text-gray-600 mt-4">
		Forgot your password?
		<a href="/auth/reset" class="text-blue-600 hover:underline">Reset it</a>
	</p>

	<p class="text-sm text-center text-gray-600 mt-2">
		Don't have an account?
		<a href="/auth/signup" class="text-blue-600 hover:underline">Sign up</a>
	</p>
</div>
