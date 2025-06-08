<script lang="ts">
	let email = "";

	const handleReset = () => {
		// Replace with actual password reset logic
		console.log("Reset password for", email);
	};
</script>

<div class="w-full max-w-sm bg-white rounded-2xl shadow-md p-6">
	<h1 class="text-2xl font-bold mb-6 text-center">Reset Password</h1>

	<form on:submit|preventDefault={handleReset} class="space-y-4">
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

		<button
			type="submit"
			class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
		>
			Send Reset Link
		</button>
	</form>

	<p class="text-sm text-center text-gray-600 mt-4">
		Remembered your password?
		<a href="/auth/login" class="text-blue-600 hover:underline">Log in</a>
	</p>
</div>
