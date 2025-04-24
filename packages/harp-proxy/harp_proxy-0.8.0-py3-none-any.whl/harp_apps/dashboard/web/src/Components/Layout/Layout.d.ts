export interface NavigationItem {
    label: string;
    to: string;
    exact?: boolean;
}
interface LayoutProps {
    title?: string;
    navigationItems: NavigationItem[];
    navBarClassName?: string;
}
declare function Layout({ title, navigationItems, navBarClassName }: LayoutProps): import("@emotion/react/jsx-runtime").JSX.Element;
export default Layout;
