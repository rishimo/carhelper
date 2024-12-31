// ColorBrewer Blues theme
export const colors = {
	// Main colors from light to dark
	blue: {
		lightest: '#eff3ff', // Background, hover states
		light: '#bdd7e7', // Secondary elements
		medium: '#6baed6', // Primary elements, notifications
		dark: '#2171b5' // Accents, important actions
	},
	// Supporting colors
	gray: {
		lightest: '#f8fafc', // Background
		light: '#e2e8f0', // Borders
		medium: '#64748b', // Secondary text
		dark: '#1e293b' // Primary text
	}
} as const;

// Common color assignments
export const theme = {
	primary: colors.blue.medium,
	primaryDark: colors.blue.dark,
	primaryLight: colors.blue.light,
	background: colors.blue.lightest,
	text: colors.gray.dark,
	textSecondary: colors.gray.medium,
	border: colors.gray.light,
	notification: colors.blue.medium
} as const;
