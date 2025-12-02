import React from 'react';

export const Button = ({ children, className = "", variant = "primary", size = "md", ...props }) => {
    const baseStyles = "inline-flex items-center justify-center rounded-xl font-medium transition-all duration-200 focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 active:scale-95";

    const variants = {
        primary: "bg-[#6366f1] text-white hover:bg-[#5558dd] shadow-lg shadow-[#6366f1]/20 border border-transparent",
        secondary: "bg-[#1a1a24] text-white border border-white/10 hover:bg-white/5",
        ghost: "bg-transparent hover:bg-white/5 text-gray-300 hover:text-white",
        outline: "border border-input bg-transparent hover:bg-accent hover:text-accent-foreground"
    };

    const sizes = {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 py-2 text-sm",
        lg: "h-12 px-8 text-base",
        icon: "h-10 w-10"
    };

    const variantStyles = variants[variant] || variants.primary;
    const sizeStyles = sizes[size] || sizes.md;

    return (
        <button
            className={`${baseStyles} ${variantStyles} ${sizeStyles} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};

export default Button;